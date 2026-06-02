from agents import Agent
from agents.sandbox import sandbox

# 创建一个数据分析 Agent
data_agent = Agent(
    name="data_analyst",
    instructions="你是一个数据分析助手。当用户需要数据分析时，使用代码执行工具进行分析并给出结果。",
    tools=[sandbox],
)

# 运行数据分析任务
response = data_agent.run("请计算 1 到 100 的所有质数之和")

# Agent 会：
# 1. 生成 Python 代码计算质数
# 2. 在 Sandbox 环境中安全执行
# 3. 返回执行结果给用户
print(response)