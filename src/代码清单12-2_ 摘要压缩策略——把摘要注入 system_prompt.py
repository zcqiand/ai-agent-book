from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)

def summarize(messages_text: str) -> str:
    """调用 LLM 把一段对话压缩成摘要。"""
    resp = llm.invoke([
        SystemMessage(content="把以下对话压缩成不超过 100 字的要点摘要。"),
        HumanMessage(content=messages_text),
    ])
    return resp.content

# 演示：当历史超过阈值时，把早期部分压缩成摘要
def chat_with_summary(messages, user_input, summary_state):
    # 若历史较长，先把已积累的对话压缩进 summary_state
    if len(messages) >= 6 and not summary_state["done"]:
        early = "\n".join(m["content"] for m in messages[:-2])
        summary_state["text"] = summarize(early)
        summary_state["done"] = True  # 简化演示，实际应滚动压缩

    messages.append({"role": "user", "content": user_input})

    # 把摘要拼进 system_prompt，让 Agent 带着压缩后的长期记忆推理
    system_prompt = (
        f"你是一个有记忆的助手。之前的对话摘要：{summary_state['text']}"
        if summary_state.get("text")
        else "你是一个有记忆的助手。"
    )
    agent = create_agent(model=llm, tools=[], system_prompt=system_prompt)
    result = agent.invoke({"messages": messages})
    reply = result["messages"][-1].content
    messages.append({"role": "assistant", "content": reply})
    return reply