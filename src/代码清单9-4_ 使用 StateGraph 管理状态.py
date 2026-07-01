from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    messages: List[BaseMessage]
    current_module: str
    retrieved_docs: List[str]
    tool_results: Dict[str, Any]

workflow = StateGraph(AgentState)

workflow.add_node("router", router_node)
workflow.add_node("rag", rag_node)
workflow.add_node("tool", tool_node)
workflow.add_node("respond", respond_node)

workflow.set_entry_point("router")
workflow.add_edge("router", "rag", condition=lambda s: s["needs_rag"])
workflow.add_edge("router", "tool", condition=lambda s: s["needs_tool"])
workflow.add_edge("rag", "respond")
workflow.add_edge("tool", "respond")
workflow.add_edge("respond", END)

app = workflow.compile()
