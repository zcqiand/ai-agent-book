from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

# 用 @tool 装饰器定义工具，LangChain 会自动提取函数签名作为 Schema
@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    # 实际项目中这里调用天气 API
    return f"{city}今天晴，25°C"

# 将工具绑定到 LLM，底层走模型原生的 tool-calling
llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_tools = llm.bind_tools([get_weather])

# 发送请求，LLM 会自动判断是否需要调用工具
response = llm_with_tools.invoke([
    HumanMessage(content="北京今天天气怎么样？")
])

# 解析工具调用
tool_calls = response.tool_calls
if tool_calls:
    for call in tool_calls:
        func_name = call["name"]         # 工具名
        func_args = call["args"]          # 已解析的参数字典
        print(f"LLM决定调用工具：{func_name}，参数：{func_args}")
        # 执行实际的工具函数
        result = get_weather.invoke(func_args)
        print(f"执行结果：{result}")