def executor_node(state: ResearchState) -> ResearchState:
    """执行节点：根据任务类型执行相应操作"""

    current_task = state["current_task"]
    topic = state["topic"]

    if "搜索" in current_task:
        result = search_task(topic, current_task)
    elif "分析" in current_task:
        result = analyze_task(state["findings"])
    elif "调研" in current_task:
        result = survey_task(topic)
    elif "整理" in current_task:
        result = organize_task(state["findings"])
    elif "撰写" in current_task:
        result = write_report(state["findings"], topic)
    else:
        result = f"完成任务：{current_task}"

    return {
        **state,
        "findings": state.get("findings", []) + [{"task": current_task, "result": result}]
    }
