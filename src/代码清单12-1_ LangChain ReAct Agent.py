from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 定义工具
def search_knowledge_base(query: str) -> str:
    """从知识库搜索"""
    return f"知识库搜索结果: {query}相关的文档..."

def get_current_date() -> str:
    """获取当前日期"""
    from datetime import date
    return str(date.today())

tools = [
    Tool(
        name="搜索知识库",
        func=search_knowledge_base,
        description="当你需要从知识库查找信息时使用"
    ),
    Tool(
        name="获取日期",
        func=get_current_date,
        description="获取当前日期，用于回答与时间相关的问题"
    )
]

# 初始化 ReAct Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.REACT_DOCSTORE,
    verbose=True
)

# 运行
result = agent.run("今天的日期是什么？请同时从知识库搜索'AI最新进展'")
print(result)
