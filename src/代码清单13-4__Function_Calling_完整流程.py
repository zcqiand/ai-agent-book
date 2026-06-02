from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)

tools = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "搜索网络信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"}
                },
                "required": ["query"]
            }
        }
    }
]

# LLM 自动判断是否需要调用工具
response = llm.invoke(
    ["用户: 帮我搜索AI的最新进展"],
    tools=tools
)

# 解析工具调用
if response.tool_calls:
    for call in response.tool_calls:
        print(f"LLM决定调用: {call.function.name}")
        print(f"参数: {call.function.arguments}")