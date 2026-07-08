from typing import TypedDict, List, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages


class AssistantState(TypedDict):
    """LangGraph 全局状态：所有节点共享读写同一份 state。

    本章只用内存级 state（进程内 dict），不展开 checkpointer 持久化——
    跨进程/跨调用续跑的能力留到卷二讲。这里关心的是「同一次 invoke 内
    多个节点怎么共享上下文」。
    """
    # 多轮记忆的载体：用 Annotated[..., add_messages] 声明 reducer，
    # 节点返回 {"messages": [AIMessage]} 会被追加而非覆盖，历史才不丢
    messages: Annotated[List[BaseMessage], add_messages]
    # 当前意图（rag/tool/chat），由 classify 节点写入、route_by_intent 读取
    intent: str
    # 当前用户输入的原文快照，方便节点直接取用，免去反复从 messages 抠
    user_input: str