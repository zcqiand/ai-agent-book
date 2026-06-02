from langgraph.graph import StateGraph, END
from typing import TypedDict, List

class ResearchState(TypedDict):
    messages: List[str]
    query: str
    iterations: int
    findings: List[str]
    final_report: str

def router_node(state: ResearchState) -> ResearchState:
    """路由节点：判断是否需要搜索"""
    return {
        **state,
        "current_step": "route"
    }

def search_node(state: ResearchState) -> ResearchState:
    """搜索节点：执行搜索"""
    query = state["query"]
    # 模拟搜索
    findings = [f"关于{query}的搜索结果..."]
    return {
        **state,
        "findings": state.get("findings", []) + findings,
        "iterations": state.get("iterations", 0) + 1
    }

def analyze_node(state: ResearchState) -> ResearchState:
    """分析节点：判断是否需要更多搜索"""
    # 模拟分析
    need_more = state.get("iterations", 0) < 3
    return {
        **state,
        "context": {"need_more_search": need_more}
    }

def respond_node(state: ResearchState) -> ResearchState:
    """响应节点：生成最终报告"""
    report = f"基于{len(state.get('findings', []))}个发现生成报告..."
    return {
        **state,
        "final_report": report
    }

# 构建图
workflow = StateGraph(ResearchState)
workflow.add_node("router", router_node)
workflow.add_node("search", search_node)
workflow.add_node("analyze", analyze_node)
workflow.add_node("respond", respond_node)

workflow.set_entry_point("router")
workflow.add_edge("router", "search")
workflow.add_edge("search", "analyze")

# 条件边：继续搜索或结束
def should_continue(state: ResearchState) -> str:
    if state.get("context", {}).get("need_more_search"):
        return "search"
    return "respond"

workflow.add_conditional_edges(
    "analyze",
    should_continue,
    {"search": "search", "respond": "respond"}
)
workflow.add_edge("respond", END)

# 编译运行
app = workflow.compile()
result = app.invoke({
    "messages": [],
    "query": "AI大模型最新进展",
    "iterations": 0,
    "findings": [],
    "final_report": ""
})

print(result["final_report"])