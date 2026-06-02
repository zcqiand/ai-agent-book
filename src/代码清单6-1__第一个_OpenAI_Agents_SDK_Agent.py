from agents import Agent

# 创建一个简单的 Agent
greeter = Agent(
    name="greeter",
    instructions="你是一个友好的客服助手，用温暖的语气问候用户并询问他们需要什么帮助。",
)

# 运行 Agent
response = greeter.run("你好，我想了解一下你们的产品")
print(response)