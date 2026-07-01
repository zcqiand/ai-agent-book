from typing import List, TypedDict

class ConversationState(TypedDict):
    messages: List[str]  # 对话历史
    context: Dict[str, Any]  # 上下文信息
    current_agent: str  # 当前 Agent

def add_memory_to_state(state: ConversationState, user_input: str, response: str) -> ConversationState:
    """将对话添加到记忆"""
    new_messages = state.get("messages", [])
    new_messages.append(f"用户: {user_input}")
    new_messages.append(f"助手: {response}")

    # 只保留最近10轮对话，防止状态膨胀
    if len(new_messages) > 20:
        new_messages = new_messages[-20:]

    return {
        **state,
        "messages": new_messages
    }

# 在 router 中使用记忆
def router_with_memory(state: ConversationState) -> str:
    """带记忆的路由"""
    history = "\n".join(state.get("messages", []))

    prompt = f"""根据对话历史和当前问题，判断应该使用哪个Agent。

    对话历史：
    {history}

    当前问题：{state.get('current_input', '')}

    请判断：rag_agent / tool_agent / general_agent"""

    result = llm.invoke(prompt)
    return result.content.strip()
