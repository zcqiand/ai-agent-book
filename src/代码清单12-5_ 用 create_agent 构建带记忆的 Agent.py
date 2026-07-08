from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 定义工具
@tool
def search(query: str) -> str:
    """搜索信息。"""
    return f"搜索结果: {query}"

# create_agent 返回 CompiledStateGraph，短期记忆由其内置 messages 状态承载
# 不再需要像 0.x 那样传入 memory=ConversationBufferMemory(...)
agent = create_agent(
    model=llm,
    tools=[search],
    system_prompt="你是一个有记忆的助手，能记住对话中提到的信息。",
    debug=True,  # 等价于旧版的 verbose=True
)

# 多轮对话：手动累积 messages 演示短期记忆原理
# （实际工程中由会话层/框架托管，开发者通常不直接操作 messages）
messages = []

def chat(user_input: str) -> str:
    messages.append({"role": "user", "content": user_input})
    result = agent.invoke({"messages": messages})
    reply = result["messages"][-1].content
    messages.append({"role": "assistant", "content": reply})
    return reply

print(chat("我叫张三"))
print(chat("帮我搜索AI的最新进展"))
print(chat("我的名字是什么？"))  # 能回答"张三"，因为名字在 messages 历史里