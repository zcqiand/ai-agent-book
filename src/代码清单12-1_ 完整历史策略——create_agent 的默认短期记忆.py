from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)

@tool
def echo(query: str) -> str:
    """原样返回输入，用于演示。"""
    return f"已收到：{query}"

# create_agent 返回一个 CompiledStateGraph，短期记忆由其内置的 messages 状态承载
agent = create_agent(
    model=llm,
    tools=[echo],
    system_prompt="你是一个有记忆的助手，能记住对话中提到的信息。",
)

# 维护一份 messages 列表作为跨轮次的短期记忆
# （实际工程中由会话层自动累积，这里手动演示原理）
messages = []

def chat_with_memory(user_input: str) -> str:
    messages.append({"role": "user", "content": user_input})
    # 每轮把完整历史传入，Agent 自动「记得」之前所有对话
    result = agent.invoke({"messages": messages})
    reply = result["messages"][-1].content
    messages.append({"role": "assistant", "content": reply})
    return reply

# 多轮对话示例
print(chat_with_memory("我叫张三"))
print(chat_with_memory("记住我叫什么了吗？"))  # 能回答"张三"