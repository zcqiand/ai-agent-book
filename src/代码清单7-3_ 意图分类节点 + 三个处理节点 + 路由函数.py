from langchain_core.messages import HumanMessage, AIMessage


def classify_intent_node(state):
    """读最后一条用户消息，用 LLM + PydanticOutputParser 判意图。

    返回 {"intent": ...} 作为 state 增量——LangGraph 会把它合并进全局 state，
    下一个节点（rag/tool/chat）就能读到 state["intent"]。
    """
    last_msg = state["messages"][-1]
    user_text = last_msg.content if hasattr(last_msg, "content") else str(last_msg)

    # 用 format_instructions 把 pydantic schema 灌进 prompt，约束 LLM 输出 JSON
    prompt = (
        f"用户说：「{user_text}」\n"
        f"请判断意图，按如下格式输出：\n"
        f"{intent_parser.get_format_instructions()}\n"
    )
    raw = llm.invoke(prompt)
    # parser 解析失败会抛 OutputParserException——教学版直接让它冒泡，
    # 生产环境应 try/except 降级为 "chat" 兜底
    parsed: IntentClassification = intent_parser.parse(raw.content)
    return {"intent": parsed.intent, "user_input": user_text}


def rag_node(state):
    """检索知识库 + LLM 生成答案。承接 ch5 的检索+生成链。"""
    answer = qa_chain.invoke({"query": state["user_input"]})
    # 追加 AIMessage 进 messages——配 add_messages reducer 后是追加而非覆盖，
    # 这是多轮记忆累积的关键
    return {"messages": [AIMessage(content=answer["result"])]}


def tool_node(state):
    """从用户输入里抠出 employee_id，调工具拿结果。"""
    user_text = state["user_input"]
    # 教学版：用最简单的子串匹配提工号；生产环境用 LLM tool_calling 结构化抽取
    emp_id = "E001"
    for token in user_text.replace("，", " ").split():
        if token.upper().startswith("E") and token[1:].isdigit():
            emp_id = token
            break
    result = query_leave_balance.invoke({"employee_id": emp_id})
    return {"messages": [AIMessage(content=result)]}


def chat_node(state):
    """无工具无检索的纯闲聊：直接让 LLM 回。"""
    reply = llm.invoke(state["messages"])
    return {"messages": [AIMessage(content=reply.content)]}


def respond_node(state):
    """出口节点：把最后一条 AIMessage 标记为最终回复。

    本节点不改变语义，只做收口——后续若要加日志/后处理/格式化，集中在这里。
    """
    return {}


def route_by_intent(state) -> str:
    """条件边路由函数：返回 state["intent"] 让 LangGraph 据此选下一条边。

    这就是替代旧版 handoffs 的条件边路由——意图字符串驱动图拓扑分流，
    而非在节点内部互相 handoff。
    """
    return state["intent"]