from agents import Agent
from agents.session import Session

# 创建 Agent
agent = Agent(
    name="assistant",
    instructions="你是一个有帮助的助手。"
)

# 创建 Session
session = Session(agent=agent)

# 多轮对话
session.run("我叫张三")
session.run("我喜欢编程")
response = session.run("我叫什么？")
print(response)  # 应该回答"张三"
