import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory

# 1. 配置 LangSmith
os.environ["LANGCHAIN_API_KEY"] = "your-key"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "debugging-agent"

# 2. 定义工具
def search_docs(query: str) -> str:
    """搜索文档"""
    return f"文档搜索结果: {query}相关的文档..."

def calculate(expression: str) -> str:
    """计算表达式"""
    try:
        result = eval(expression)
        return str(result)
    except:
        return "计算错误"

tools = [
    Tool(name="搜索文档", func=search_docs, description="搜索公司文档"),
    Tool(name="计算器", func=calculate, description="执行数学计算")
]

# 3. 创建带记忆的 Agent
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = initialize_agent(
    tools=tools,
    llm=ChatOpenAI(model="gpt-4", temperature=0),
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=False
)

# 4. 运行测试
test_queries = [
    "搜索关于AI的文档",
    "计算 123 * 456",
    "我之前搜索了什么？"
]

for query in test_queries:
    print(f"Query: {query}")
    result = agent.run(query)
    print(f"Result: {result}")
    print("-" * 50)

# 5. 在 LangSmith 查看追踪
print("查看追踪: https://smith.langchain.com/")
