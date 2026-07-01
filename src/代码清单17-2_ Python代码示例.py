from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 定义工具
def search_tool(query: str) -> str:
    return f"搜索结果: {query}..."

tools = [Tool(name="搜索", func=search_tool, description="搜索信息")]

# 创建 Agent（启用追踪）
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=False  # LangSmith会记录，不需要verbose
)

# 运行 - 自动被追踪
result = agent.run("AI的最新发展是什么？")

# 在 LangSmith Dashboard 查看完整轨迹
print("查看 https://smith.langchain.com/")
