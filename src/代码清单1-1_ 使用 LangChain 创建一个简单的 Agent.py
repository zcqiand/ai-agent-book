from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI

# 初始化 LLM（需要设置 OPENAI_API_KEY 环境变量）
llm = ChatOpenAI(model="gpt-4", temperature=0)

# 自写一个简易计算器工具：@tool 装饰器把普通函数登记为 LangChain 工具
@tool
def calculator(expression: str) -> str:
    """计算一个数学表达式并返回结果，例如 '3 * 12 + 5'。"""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"计算失败：{e}"

# 准备工具列表：搜索（社区包，运行时需 pip install duckduckgo-search）+ 计算器
tools = [DuckDuckGoSearchRun(), calculator]

# 1.x 推荐：用 create_agent 构造一个基于 tool-calling 的 Agent
# system_prompt 注入角色设定；debug=True 打印每一步执行轨迹（等价于旧版的 verbose）
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="你是一个能调用搜索和计算器工具的助手。",
    debug=True,
)

# 让 Agent 回答一个需要工具调用的问题
result = agent.invoke({
    "messages": [{"role": "user", "content": "北京现在的温度是多少？与上海相比如何？"}]
})
print(result["messages"][-1].content)