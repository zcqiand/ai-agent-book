from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 用 @tool 装饰器把普通函数登记为 LangChain 工具
# 函数签名 + docstring 自动成为工具的参数 schema 和描述
@tool
def search_knowledge_base(query: str) -> str:
    """当你需要从知识库查找信息时使用。"""
    return f"知识库搜索结果: {query}相关的文档..."

@tool
def get_current_date() -> str:
    """获取当前日期，用于回答与时间相关的问题。"""
    from datetime import date
    return str(date.today())

tools = [search_knowledge_base, get_current_date]

# 用 create_agent 构造一个基于 tool-calling 的 ReAct Agent
# system_prompt 注入角色设定；debug=True 打印每一步执行轨迹（等价于旧版的 verbose）
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="你是一个能调用知识库搜索和日期查询工具的助手。",
    debug=True,
)

# 运行：create_agent 返回一个 LangGraph CompiledStateGraph，
# invoke 时传 messages，取最后一条消息的 content 即为最终回答
result = agent.invoke({
    "messages": [{"role": "user", "content": "今天的日期是什么？请同时从知识库搜索'AI最新进展'"}]
})
print(result["messages"][-1].content)