from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, END, StateGraph


class HitlState(TypedDict):
    """本章演示用的最小状态。

    用 TypedDict 声明字段。本章不引入 messages 列表——HITL 演示只需要
    「内容」+「是否放行」两个标量字段，没必要背一份多轮历史进来，保持示例最小化。
    """
    # 用户原始输入；generate 节点读它做草稿
    user_input: str
    # generate 产出的草稿内容；human_review 之前已经填好，暂停时就是给人看的待审稿
    generated_content: str
    # 人审结果：True=放行，False=未放行。初值 False——暂停时这一项还是 False，
    # 这正是「不能拿 approved 判暂停」的原因（见代码清单20-2 的注释）
    approved: bool


def generate(state: HitlState) -> dict:
    """草稿生成节点（纯 echo，不调 LLM）。

    用方括号包一下用户输入做草稿——演示用。真实场景这里会调 LLM 产邮件/回复/工单。
    把 user_input 包成 generated_content 是为了让暂停时 snapshot.values 能直接看到「待审稿长什么样」。
    """
    return {"generated_content": f"[草稿] {state['user_input']}"}


def human_review(state: HitlState) -> dict:
    """人审放行节点。

    把 approved 置 True 模拟「人审通过」。
    真实生产场景里这一步不应该是自动函数——它应该是「外部人审系统把结果写回 state」
    （用 update_state，见代码清单20-3）；本演示为了让图能跑通、不引入外部系统，放一个自动节点占位。
    重点在「这一节点被 interrupt_before 拦住、暂停在它之前」这个机制，不在它内部逻辑。
    """
    return {"approved": True}


def execute(state: HitlState) -> dict:
    """放行执行节点。

    approved=True 才会到这里（human_review 之后）。把草稿内容标记成「已发送」模拟下游投递。
    """
    return {"generated_content": f"[已发送] {state['generated_content']}"}


def build_graph(checkpointer):
    """编译并返回带人审中断的图。

    关键一行：compile(interrupt_before=['human_review'], checkpointer=checkpointer)。
    - interrupt_before=['human_review']：图在执行到 human_review 之前真暂停（不出 END），
      状态由 checkpointer 落盘——这是本章的核心 API。
    - checkpointer：MemorySaver 是开发调试用（同进程内演示 interrupt 最省力，
      不建文件、不连数据库）。生产场景换成 SqliteSaver / PostgresSaver，图代码一行不动。
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
        interrupt_before=["human_review"],
        checkpointer=checkpointer,
    )


if __name__ == "__main__":
    # MemorySaver：langgraph 内置，零外部依赖，同进程演示 interrupt 机制最省力
    saver = MemorySaver()
    graph = build_graph(saver)
    print("图已建好，节点列表:", list(graph.get_graph().nodes))
    # 本清单不 invoke——invoke 后会停在 human_review 之前，演示在代码清单20-2