from langchain.agents import AgentType, initialize_agent, load_tools
from langchain_openai import ChatOpenAI

# 初始化 LLM（需要设置 OPENAI_API_KEY 环境变量）
llm = ChatOpenAI(model="gpt-4", temperature=0)

# 加载内置工具：搜索和计算
tools = load_tools(["search", "calculator"])

# 创建 Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 让 Agent 回答一个需要工具调用的问题
result = agent.run("北京现在的温度是多少？与上海相比如何？")
print(result)