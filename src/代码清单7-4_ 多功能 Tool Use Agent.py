from anthropic import Anthropic

client = Anthropic()

tools = [
    {
        "name": "calculator",
        "description": "进行数学计算，支持加减乘除和括号",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "数学表达式，如 2+3*4"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "get_weather",
        "description": "获取城市天气",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名"}
            },
            "required": ["city"]
        }
    }
]

def execute_tool(tool_name, tool_input):
    """执行工具调用"""
    if tool_name == "calculator":
        try:
            result = eval(tool_input["expression"])
            return str(result)
        except:
            return "计算错误"
    elif tool_name == "get_weather":
        return f"{tool_input['city']}今天晴，温度20度"
    return "未知工具"

def chat_with_agent(user_input, conversation_history=None):
    """与 Agent 对话"""
    if conversation_history is None:
        conversation_history = []

    messages = conversation_history + [{"role": "user", "content": user_input}]

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=messages,
        tools=tools,
    )

    # 处理工具调用
    while response.stop_reason == "tool_use":
        for content in response.content:
            if content.type == "tool_use":
                result = execute_tool(content.name, content.input)

                # 将工具结果加入对话
                messages.append({"role": "assistant", "content": response.content[0].text if response.content else ""})
                messages.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": content.id,
                        "content": result
                    }]
                })

                # 继续对话
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1024,
                    messages=messages,
                    tools=tools,
                )

    return response.content[0].text, messages

# 运行示例
result, history = chat_with_agent("北京今天天气如何？另外帮我算一下 123*456")
print(result)
