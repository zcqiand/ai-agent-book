import os
import tempfile

from langgraph.checkpoint.sqlite import SqliteSaver

# from listing_19_1 import DemoState, echo_node


def build_graph():
    graph_builder = StateGraph(DemoState)
    graph_builder.add_node("echo", echo_node)
    graph_builder.add_edge(START, "echo")
    graph_builder.add_edge("echo", END)
    return graph_builder


def write_checkpoint(db_path: str, config: dict) -> dict:
    """第一个 with 块：建图 + invoke 落盘，然后退出 with（关连接）。

    with 块结束意味着 SqliteSaver 底层的 sqlite3 连接被关闭——
    如果状态只活在内存里，这一步之后状态就没了。本函数验证的是「状态已落盘到文件」。
    """
    with SqliteSaver.from_conn_string(db_path) as saver:
        graph = build_graph().compile(checkpointer=saver)
        init_state = {
            "messages": [HumanMessage(content="进程A写的消息")],
            "user_input": "进程A写的消息",
            "turn_count": 0,
        }
        result = graph.invoke(init_state, config)
        print(f"[写入] turn_count={result['turn_count']}, "
              f"messages 长度={len(result['messages'])}")
        return result


def read_and_continue(db_path: str, config: dict) -> dict:
    """第二个 with 块：用同一个 db 文件 + 同一个 thread_id，开新连接。

    与第一个 with 块的唯一联系是 db_path（同一个 SQLite 文件）和 thread_id（同一个键）。
    进了全新的 with、全新建的 saver、全新编译的 graph 对象——
    如果 checkpointer 真把状态落盘了，这里 invoke 应该能读到上次的 turn_count=1 并续跑。
    """
    with SqliteSaver.from_conn_string(db_path) as saver:
        graph = build_graph().compile(checkpointer=saver)

        # 先不 invoke，直接 get_state 看看新连接能不能读到上次的快照
        snapshot = graph.get_state(config)
        print(f"[读回] get_state 拿到 turn_count={snapshot.values.get('turn_count')}")

        # 再 invoke 一次新消息，看 turn_count 是从 0 起步（没恢复）还是从 1 续跑（恢复了）
        result = graph.invoke(
            {"messages": [HumanMessage(content="进程B的追问")],
             "user_input": "进程B的追问"},
            config,
        )
        print(f"[续跑] turn_count={result['turn_count']}, "
              f"messages 长度={len(result['messages'])}")
        return result


def main():
    # 同一个 db 文件贯穿两个 with 块——这是「跨连接存活」的物理基础
    tmp_dir = tempfile.mkdtemp(prefix="ch19_cross_")
    db_path = os.path.join(tmp_dir, "checkpoints.db")
    config = {"configurable": {"thread_id": "demo-cross"}}

    write_checkpoint(db_path, config)
    # 此处第一个 with 已退出，sqlite3 连接已关闭
    read_and_continue(db_path, config)

    # 旁证：db 文件确实有内容（不是空文件、不是只在内存）
    db_size = os.path.getsize(db_path)
    print(f"[旁证] db 文件大小: {db_size} 字节（非 0 = 状态真的落盘了）")


if __name__ == "__main__":
    main()