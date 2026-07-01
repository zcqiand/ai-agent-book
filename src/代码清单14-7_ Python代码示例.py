from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.tools import Tool

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 工具
def search_homework(topic: str) -> str:
    """搜索作业信息"""
    return f"作业: 关于{topic}的数学作业已完成批改"

tools = [Tool(name="查作业", func=search_homework, description="查询学生作业情况")]

# 记忆
memory = ConversationBufferMemory(
    memory_key="student_history",
    return_messages=True
)

# Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# 运行示例
print(agent.run("我是李明，班级初一(2)班"))
print(agent.run("我的数学作业完成情况如何？"))
print(agent.run("我是谁？记住我叫什么名字？"))
