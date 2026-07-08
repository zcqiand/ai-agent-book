from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)
agent = create_agent(model=llm, tools=[], system_prompt="你是一个有记忆的助手。")

WINDOW_K = 5  # 只保留最近5轮（每轮=1条user+1条assistant，共10条消息）

def chat_with_window(messages, user_input):
    messages.append({"role": "user", "content": user_input})
    # 窗口切片：只把最近 WINDOW_K*2 条消息传给 Agent
    recent = messages[-(WINDOW_K * 2):]
    result = agent.invoke({"messages": recent})
    reply = result["messages"][-1].content
    messages.append({"role": "assistant", "content": reply})
    return reply

# 超过5轮后，最早的对话不会进入 Agent 的上下文
messages = []
for i in range(10):
    chat_with_window(messages, f"用户消息{i}")
print(f"完整历史{len(messages)}条，但 Agent 每轮只见最近{WINDOW_K*2}条")