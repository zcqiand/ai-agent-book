from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Annotated
import operator

class ConversationState(TypedDict):
    messages: Annotated[List[str], operator.add]
    context: dict
    current_agent: str
    should_end: bool

def greeting_node(state: ConversationState) -> ConversationState:
    """问候节点"""
    return {
        **state,
        "messages": state["messages"] + ["助手: 你好，有什么可以帮助你的？"]
    }

def understanding_node(state: ConversationState) -> ConversationState:
    """理解用户意图"""
    last_msg = state["messages"][-1] if state["messages"] else ""
    # 模拟意图识别
    intent = "general"
    return {
        **state,
        "context": {"intent": intent}
    }

def route_based_on_intent(state: ConversationState) -> str:
    """根据意图路由"""
    intent = state.get("context", {}).get("intent", "general")
    if intent == "search":
        return "search_agent"
    elif intent == "tool":
        return "tool_agent"
    else:
        return "general_agent"

def general_agent_node(state: ConversationState) -> ConversationState:
    """通用 Agent 节点"""
    return {
        **state,
        "messages": state["messages"] + ["助手: 我来帮你解答这个问题。"]
    }

def search_agent_node(state: ConversationState) -> ConversationState:
    """搜索 Agent 节点"""
    return {
        **state,
        "messages": state["messages"] + ["助手: 让我搜索一下相关信息。"]
    }

def tool_agent_node(state: ConversationState) -> ConversationState:
    """工具 Agent 节点"""
    return {
        **state,
        "messages": state["messages"] + ["助手: 我来调用工具帮你处理。"]
    }

# 构建图
workflow = StateGraph(ConversationState)
workflow.add_node("greeting", greeting_node)
workflow.add_node("understand", understanding_node)
workflow.add_node("general", general_agent_node)
workflow.add_node("search", search_agent_node)
workflow.add_node("tool", tool_agent_node)

workflow.set_entry_point("greeting")
workflow.add_edge("greeting", "understand")
workflow.add_conditional_edges(
    "understand",
    route_based_on_intent,
    {
        "general": "general",
        "search": "search",
        "tool": "tool"
    }
)
workflow.add_edge("general", END)
workflow.add_edge("search", END)
workflow.add_edge("tool", END)

# 运行
app = workflow.compile()
result = app.invoke({
    "messages": ["用户: 我想了解 AI 的最新进展"],
    "context": {},
    "current_agent": "unknown",
    "should_end": False
})

for msg in result["messages"]:
    print(msg)