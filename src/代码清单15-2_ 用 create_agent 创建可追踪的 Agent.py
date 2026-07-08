from langchain_openai import ChatOpenAI
from langchain.agents import create_agent  # LangChain 1.x：create_agent 取代 initialize_agent
from langchain_core.tools import tool

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 定义工具：用 @tool 装饰器（1.x 推荐写法，自动从签名和 docstring 推断 schema）
@tool
def search(query: str) -> str:
    """搜索信息"""
    return f"搜索结果: {query}..."

# 创建 Agent（环境变量配好后，所有 LLM/工具调用自动进 LangSmith 追踪）
agent = create_agent(
    model=llm,
    tools=[search],
)

# 运行 —— create_agent 返回的是 LangGraph CompiledStateGraph，入参用 messages
result = agent.invoke({"messages": [{"role": "user", "content": "AI的最新发展是什么？"}]})
print(result["messages"][-1].content)

# 在 LangSmith Dashboard 查看完整轨迹
print("查看 https://smith.langchain.com/")