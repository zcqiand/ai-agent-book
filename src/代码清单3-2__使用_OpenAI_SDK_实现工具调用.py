from openai import OpenAI

client = OpenAI()

# 定义工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# 发送请求，LLM会自动判断是否需要调用工具
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "北京今天天气怎么样？"}],
    tools=tools
)

# 解析工具调用
tool_calls = response.choices[0].message.tool_calls
if tool_calls:
    for call in tool_calls:
        func_name = call.function.name
        func_args = eval(call.function.arguments)  # 解析JSON参数
        print(f"LLM决定调用工具：{func_name}，参数：{func_args}")
        # 在这里执行实际的工具函数
        # result = get_weather(func_args["city"])