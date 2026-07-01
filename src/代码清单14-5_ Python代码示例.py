from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.tools import Tool

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 定义工具
def search_tool(query: str) -> str:
    return f"搜索结果: {query}"

tools = [Tool(name="搜索", func=search_tool, description="搜索信息")]

# 创建记忆
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 初始化带记忆的 Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,  # 传入记忆
    verbose=True
)

# 多轮对话
agent.run("我叫张三")
agent.run("帮我搜索AI的最新进展")
agent.run("我的名字是什么？")  # 能回答"张三"
