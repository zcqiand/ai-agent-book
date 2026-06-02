
# 普通边：线性执行
workflow.add_edge("search", "analyze")
workflow.add_edge("analyze", "respond")
workflow.add_edge("respond", END)

# 条件边：根据状态决定下一步
def should_continue(state: AgentState) -> str:
    """判断是否需要继续搜索"""
    if state.get("context", {}).get("need_more_search"):
        return "search"
    else:
        return "respond"

workflow.add_conditional_edges(
    "router",
    should_continue,
    {
        "search": "search",
        "respond": "respond"
    }
)

### 编译并运行图