from typing import List, TypedDict, Annotated

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages


class DemoState(TypedDict):
    """本章演示用的最小状态。

    承接第7章 AssistantState 的写法：messages 字段用 Annotated[..., add_messages]
    声明 reducer，节点返回的 {"messages": [msg]} 是追加而不是覆盖，多轮历史才不丢。
    本章不引入 CSState（那是第26章客服案例的状态类）。
    """
    # 多轮记忆载体：reducer=add_messages 把默认的「覆盖」改成「追加」语义
    messages: Annotated[List[BaseMessage], add_messages]
    # 当前这一轮用户输入的原文快照，节点直接取用，免去反复从 messages 里抠
    user_input: str
    # 对话轮次计数：每次 echo_node 把它 +1，用来直观观察状态是否被正确累加
    turn_count: int


def echo_node(state: DemoState) -> dict:
    """把用户输入回显成一条 AIMessage，并把轮次 +1。

    纯函数写法：入参是完整 state，返回值是 partial state（只含要更新的字段）。
    不调 LLM——本章重点在持久化机制，不在 LLM 交互，去掉 LLM 让示例无 API Key 也能跑。
    """
    # 用 state 里现有的 turn_count 加 1，没传过就当 0 起步（.get 兜底默认值）
    new_count = state.get("turn_count", 0) + 1
    return {
        # 注意是列表包一条消息——add_messages reducer 会把它拼到既有 messages 末尾
        "messages": [AIMessage(content=f"[echo #{new_count}] {state['user_input']}")],
        "turn_count": new_count,
    }


def build_graph():
    """编译并返回一个最小图：START → echo_node → END。

    本清单不挂 checkpointer——先展示内存级基线，下一清单再升级到持久化。
    对比点是：没有 checkpointer 时，每次 invoke 都是孤立的一次运行。
    """
    graph = StateGraph(DemoState)
    graph.add_node("echo", echo_node)
    graph.add_edge(START, "echo")
    graph.add_edge("echo", END)
    # 不传 checkpointer=：进程一退出 state 全丢，这是第7章内存级 state 的同款局限
    return graph.compile()


if __name__ == "__main__":
    graph = build_graph()
    init_state = {
        "messages": [HumanMessage(content="你好")],
        "user_input": "你好",
        "turn_count": 0,
    }
    result = graph.invoke(init_state)

    print("messages 长度:", len(result["messages"]))
    print("turn_count:", result["turn_count"])
    print("最后一条:", result["messages"][-1].content)