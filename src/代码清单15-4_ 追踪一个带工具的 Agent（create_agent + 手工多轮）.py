import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent  # 1.x：取代 initialize_agent
from langchain_core.tools import tool

# 1. 配置 LangSmith（配好后下面所有 LLM/工具调用自动进追踪）
os.environ["LANGCHAIN_API_KEY"] = "your-key"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "debugging-agent"

# 2. 定义工具：@tool 装饰器从签名 + docstring 自动推断 schema
@tool
def search_docs(query: str) -> str:
    """搜索公司文档"""
    return f"文档搜索结果: {query}相关的文档..."

@tool
def calculate(expression: str) -> str:
    """执行数学计算"""
    try:
        return str(eval(expression))
    except Exception:
        return "计算错误"

# 3. 创建 Agent（create_agent 不再有 AgentType 枚举，也不再有 memory 参数）
agent = create_agent(
    model=ChatOpenAI(model="gpt-4", temperature=0),
    tools=[search_docs, calculate],
)

# 4. 多轮对话：对话历史自己用一个 messages 列表维护（1.x 的标准做法）
messages = []
test_queries = [
    "搜索关于AI的文档",
    "计算 123 * 456",
    "我之前搜索了什么？"  # 这一句依赖前两轮的上下文
]

for query in test_queries:
    print(f"Query: {query}")
    messages.append({"role": "user", "content": query})
    # 每轮把完整 messages 传入；agent 返回的新消息追加进列表，形成记忆
    result = agent.invoke({"messages": messages})
    answer = result["messages"][-1].content
    messages.append({"role": "assistant", "content": answer})
    print(f"Result: {answer}")
    print("-" * 50)

# 5. 在 LangSmith 查看每次 invoke 的完整轨迹（含工具调用、token、延迟）
print("查看追踪: https://smith.langchain.com/")