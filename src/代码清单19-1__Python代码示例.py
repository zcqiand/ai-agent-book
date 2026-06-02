from typing import TypedDict, List

class ResearchState(TypedDict):
    topic: str                    # 研究主题
    research_plan: List[str]      # 研究计划（子任务列表）
    current_task: str             # 当前任务
    completed_tasks: List[str]    # 已完成任务
    findings: List[dict]          # 发现
    report: str                   # 最终报告
    iteration: int                # 迭代次数

def planner_node(state: ResearchState) -> ResearchState:
    """规划节点：分析主题，生成研究计划"""
    topic = state["topic"]

    # LLM 分析主题并生成研究计划
    plan_prompt = f"""
    研究主题：{topic}

    请分析这个主题，生成5-8个研究子任务，形成研究计划。
    每个子任务应该：
    1. 具体可执行
    2. 有明确的交付物
    3. 按逻辑顺序排列

    返回格式：JSON 数组，每个元素是一个子任务描述
    """

    # 调用 LLM 生成计划
    plan = llm.invoke(plan_prompt)

    # 解析计划（简化处理）
    tasks = ["搜索背景资料", "分析核心概念", "调研最新进展", "整理案例", "撰写报告"]

    return {
        **state,
        "research_plan": tasks,
        "current_task": tasks[0] if tasks else "",
        "iteration": 0
    }