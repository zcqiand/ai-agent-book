from langgraph.graph import StateGraph, END

# 创建图，指定状态模式
workflow = StateGraph(AgentState)

# 添加节点
workflow.add_node("router", router_node)
workflow.add_node("search", search_node)
workflow.add_node("analyze", analyze_node)
workflow.add_node("respond", respond_node)

# 设置入口点
workflow.set_entry_point("router")