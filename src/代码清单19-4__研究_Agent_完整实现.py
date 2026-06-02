from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from langchain_openai import ChatOpenAI
from langchain.tools import Tool

llm = ChatOpenAI(model="gpt-4", temperature=0)

class ResearchState(TypedDict):
    topic: str
    research_plan: List[str]
    current_task: str
    completed_tasks: List[str]
    findings: List[dict]
    report: str
    should_continue: bool
    iteration: int

def planner(state: ResearchState) -> ResearchState:
    """规划"""
    return {
        **state,
        "research_plan": ["搜索背景", "分析概念", "调研进展", "整理案例", "撰写报告"],
        "current_task": "搜索背景",
        "iteration": 0
    }

def executor(state: ResearchState) -> ResearchState:
    """执行"""
    task = state["current_task"]
    result = f"执行完成: {task}"

    return {
        **state,
        "findings": state.get("findings", []) + [{"task": task, "result": result}],
        "completed_tasks": state.get("completed_tasks", []) + [task]
    }

def next_task(state: ResearchState) -> str:
    """选择下一个任务"""
    plan = state.get("research_plan", [])
    completed = state.get("completed_tasks", [])
    remaining = [t for t in plan if t not in completed]

    if remaining:
        return remaining[0]
    return END

def should_continue(state: ResearchState) -> bool:
    """判断是否继续"""
    if state.get("iteration", 0) >= 3:
        return False
    plan = state.get("research_plan", [])
    completed = state.get("completed_tasks", [])
    return len(completed) < len(plan)

# 构建图
workflow = StateGraph(ResearchState)
workflow.add_node("planner", planner)
workflow.add_node("executor", executor)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "executor")

# 条件边：继续执行或结束
workflow.add_conditional_edges(
    "executor",
    lambda state: state.get("completed_tasks", [])[-1] if state.get("completed_tasks") else None,
    {
        "撰写报告": END,
        "default": "executor"
    }
)

# 简化的路由
def route_after_executor(state: ResearchState) -> str:
    completed = state.get("completed_tasks", [])
    plan = state.get("research_plan", [])

    if len(completed) >= len(plan):
        return END

    remaining = [t for t in plan if t not in completed]
    if remaining:
        return "executor"
    return END

workflow.add_conditional_edges(
    "executor",
    route_after_executor,
    {"continue": "executor", END: END}
)

app = workflow.compile()

# 运行
result = app.invoke({
    "topic": "AI大模型在医疗领域的应用",
    "research_plan": [],
    "current_task": "",
    "completed_tasks": [],
    "findings": [],
    "report": "",
    "should_continue": True,
    "iteration": 0
})

print(f"研究完成，发现数量: {len(result.get('findings', []))}")