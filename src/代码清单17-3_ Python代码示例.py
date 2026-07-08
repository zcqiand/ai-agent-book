def evaluator_node(state: ResearchState) -> ResearchState:
    """评估节点：判断是否需要继续迭代"""

    completed = state.get("completed_tasks", [])
    plan = state.get("research_plan", [])
    iteration = state.get("iteration", 0)

    # 检查是否所有任务都完成了
    if len(completed) >= len(plan):
        return {
            **state,
            "should_continue": False
        }

    # 检查迭代次数是否超限
    if iteration >= 5:
        return {
            **state,
            "should_continue": False
        }

    # 检查是否有新发现
    recent_findings = state.get("findings", [])[-3:]
    if not recent_findings:
        return {
            **state,
            "should_continue": False
        }

    return {
        **state,
        "should_continue": True
    }