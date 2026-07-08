from langgraph.graph import StateGraph, END

# 1) 建图，状态类型用代码清单7-1 的 AssistantState
workflow = StateGraph(AssistantState)

# 2) 注册五个节点
workflow.add_node("classify", classify_intent_node)
workflow.add_node("rag", rag_node)
workflow.add_node("tool", tool_node)
workflow.add_node("chat", chat_node)
workflow.add_node("respond", respond_node)

# 3) 入口固定从意图分类开始
workflow.set_entry_point("classify")

# 4) 条件边：按 route_by_intent 返回值分流（替代旧版 handoffs）
workflow.add_conditional_edges(
    "classify",
    route_by_intent,
    {"rag": "rag", "tool": "tool", "chat": "chat"},
)

# 5) 三个处理节点汇流到 respond 收口
workflow.add_edge("rag", "respond")
workflow.add_edge("tool", "respond")
workflow.add_edge("chat", "respond")
workflow.add_edge("respond", END)

# 6) 编译成可执行图
app = workflow.compile()


# === 第一轮：查年假政策（命中 rag 分支）===
turn1 = app.invoke({
    "messages": [HumanMessage(content="公司年假政策是什么？")],
    "intent": "",
    "user_input": "",
})
print("第一轮回复：", turn1["messages"][-1].content)
# 预期：类似「入职满1年享有5天年假，满3年10天，满10年15天。」


# === 第二轮：追问请假余额（命中 tool 分支），体现多轮记忆 ===
# 关键：messages 带上第一轮全部历史，add_messages reducer 自动累积
turn2 = app.invoke({
    "messages": turn1["messages"] + [HumanMessage(content="那我工号E001还能请几天？")],
    "intent": "",
    "user_input": "",
})
print("第二轮回复：", turn2["messages"][-1].content)
# 预期：「员工E001年假余额：10天」