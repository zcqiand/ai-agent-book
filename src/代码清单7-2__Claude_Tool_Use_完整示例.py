from anthropic import Anthropic
from typing import Literal

client = Anthropic()

# 定义工具
tools = [
    {
        "name": "get_weather",
        "description": "获取指定城市的天气信息",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称，中文或英文"
                }
            },
            "required": ["city"]
        }
    }
]

# 发送消息并启用工具
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "北京今天天气怎么样？"}
    ],
    tools=tools,
)

# 检查是否有工具调用
if message.stop_reason == "tool_use":
    for content in message.content:
        if content.type == "tool_use":
            tool_name = content.name
            tool_input = content.input
            print(f"Claude 决定调用工具: {tool_name}")
            print(f"参数: {tool_input}")

            # 在这里执行实际的工具函数
            # weather = get_weather(tool_input["city"])

            # 将工具结果返回给 Claude
            tool_result = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": "北京今天天气怎么样？"},
                    message,
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": content.id,
                                "content": "北京今天晴，温度15-25度，适宜户外活动"
                            }
                        ]
                    }
                ],
                tools=tools,
            )
            print(tool_result.content[0].text)