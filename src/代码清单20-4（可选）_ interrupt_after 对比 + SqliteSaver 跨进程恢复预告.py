import os
import tempfile

from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, END, StateGraph

# 复用代码清单20-1 的 HitlState、generate、human_review、execute
# from listing_20_1 import HitlState, generate, human_review, execute


# === 第一段：interrupt_before vs interrupt_after 的语义对照 ===

def build_graph_after(checkpointer):
    """同一张图，换成 interrupt_after=['generate']。

    语义对比：
    - interrupt_before=['human_review']：执行到 human_review 之前暂停（human_review 还没跑）。
    - interrupt_after=['generate']：执行完 generate 之后暂停（generate 跑过了、human_review 没跑）。

    本清单 invoke 一次后 snapshot.next 预期也是 ('human_review',)——
    因为图的拓扑是 generate → human_review，「generate 之后」和「human_review 之前」指向同一个间隙。
    这两个 API 在这张图上同构，但语义起点不同：before 是「看着下一节点暂停」、after 是「看着刚跑完的节点暂停」。
    选哪个看业务语义——「这步是给下一节点做闸门」用 before，「这步刚跑完要复核结果」用 after。
    生产里更常见的是 before（在「会改 state 的危险节点」前拦一下），after 多用于「产出后立刻审计」。
    """
    graph_builder = StateGraph(HitlState)
    graph_builder.add_node("generate", generate)
    graph_builder.add_node("human_review", human_review)
    graph_builder.add_node("execute", execute)
    graph_builder.add_edge(START, "generate")
    graph_builder.add_edge("generate", "human_review")
    graph_builder.add_edge("human_review", "execute")
    graph_builder.add_edge("execute", END)
    return graph_builder.compile(
        interrupt_after=["generate"],   # 注意这里换成 after + generate
        checkpointer=checkpointer,
    )


def demo_interrupt_after():
    """演示 interrupt_after：generate 跑完后暂停。"""
    graph = build_graph_after(MemorySaver())
    config = {"configurable": {"thread_id": "demo-after"}}
    init_state = {"user_input": "测试 after 暂停", "generated_content": "", "approved": False}
    graph.invoke(init_state, config)

    snapshot = graph.get_state(config)
    print("[after] snapshot.next:", snapshot.next)
    print("[after] generated_content:", snapshot.values.get("generated_content"))
    print("[after] approved:", snapshot.values.get("approved"))


# === 第二段：SqliteSaver 跨进程恢复预告（生产级形态）===

def build_graph_sqlite():
    """与代码清单20-1 同构的 graph_builder，留给 with 块挂 SqliteSaver。

    不在函数内 compile——SqliteSaver 要进上下文（from_conn_string 是上下文管理器工厂，
    必须用 with 取出 yield 出来的 saver），所以编译挪到 with 块内做。
    """
    graph_builder = StateGraph(HitlState)
    graph_builder.add_node("generate", generate)
    graph_builder.add_node("human_review", human_review)
    graph_builder.add_node("execute", execute)
    graph_builder.add_edge(START, "generate")
    graph_builder.add_edge("generate", "human_review")
    graph_builder.add_edge("human_review", "execute")
    graph_builder.add_edge("execute", END)
    return graph_builder


def write_checkpoint_hitl(db_path: str, config: dict):
    """第一个 with 块：建图 + invoke 到 human_review 之前暂停，状态落盘到 SQLite 文件。

    SqliteSaver 与 MemorySaver 的本质差异就在这里：暂停时 state 不会随进程退出而消失，
    而是被 checkpointer 写进 db_path 这个 SQLite 文件——这正是「跨进程恢复」的物理基础。
    本函数结束时 with 块退出、sqlite3 连接关闭、Python 进程内 state 全没了，
    但 db_path 文件里那条 checkpoint 还在。
    """
    with SqliteSaver.from_conn_string(db_path) as saver:
        graph = build_graph_sqlite().compile(
            interrupt_before=["human_review"],
            checkpointer=saver,
        )
        init_state = {"user_input": "跨连接的 HITL 演示", "generated_content": "", "approved": False}
        graph.invoke(init_state, config)
        snapshot = graph.get_state(config)
        print(f"[进程A 写入] snapshot.next={snapshot.next}, "
              f"generated_content={snapshot.values.get('generated_content')!r}")


def read_and_continue_hitl(db_path: str, config: dict):
    """第二个 with 块：开新连接、用同 db_path + 同 thread_id 续跑。

    与第一个 with 块的唯一联系是 db_path（同一 SQLite 文件）和 thread_id（同一键）——
    进了全新的 with、全新建的 saver、全新编译的 graph 对象。
    checkpointer 按 thread_id 从文件读回暂停时的快照，invoke(None, config) 从断点续跑后半段。
    这正是 ch26 客服场景的生产级形态：客服系统进程 A 调图到人审前暂停（状态落库），
    人审系统进程 B 审批通过后调 invoke(None, config) 续跑投递——两个进程不共享内存，只共享数据库。
    """
    with SqliteSaver.from_conn_string(db_path) as saver:
        graph = build_graph_sqlite().compile(
            interrupt_before=["human_review"],
            checkpointer=saver,
        )
        # 先 get_state 验证：新连接能不能读到进程A 落盘的暂停快照
        snapshot = graph.get_state(config)
        print(f"[进程B 读回] snapshot.next={snapshot.next}, "
              f"generated_content={snapshot.values.get('generated_content')!r}")

        # 模拟人审通过：跨连接 update_state 写回 approved=True
        graph.update_state(config, {"approved": True})
        # 续跑：invoke(None, config) 从断点跑 human_review → execute → END
        result = graph.invoke(None, config)
        print(f"[进程B 续跑] generated_content={result.get('generated_content')!r}, "
              f"approved={result.get('approved')}")
        print(f"[进程B 续跑] snapshot.next={graph.get_state(config).next}（空元组=已到 END）")


def main():
    print("=== 第一段：interrupt_after 对比 ===")
    demo_interrupt_after()

    print("\n=== 第二段：SqliteSaver 跨进程恢复 ===")
    tmp_dir = tempfile.mkdtemp(prefix="ch20_hitl_")
    db_path = os.path.join(tmp_dir, "checkpoints.db")
    config = {"configurable": {"thread_id": "demo-cross-hitl"}}

    write_checkpoint_hitl(db_path, config)
    # 此处第一个 with 已退出，sqlite3 连接已关闭、Python state 已 GC
    read_and_continue_hitl(db_path, config)

    # 旁证：db 文件确实有内容（不是只在内存）
    print(f"[旁证] db 文件大小: {os.path.getsize(db_path)} 字节（非 0 = 状态真的落盘了）")


if __name__ == "__main__":
    main()