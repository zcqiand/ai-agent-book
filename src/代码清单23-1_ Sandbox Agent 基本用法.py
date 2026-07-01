from agents import Agent
from agents.sandbox import sandbox

# 创建一个数据分析 Agent
data_agent = Agent(
    name="data_analyst",
    instructions="你是一个数据分析助手。当用户需要数据分析时，使用代码执行工具进行分析并给出结果。",
    tools=[sandbox],  # 配备 Sandbox 工具
)

# 运行数据分析任务
response = data_agent.run("请分析一下这个CSV文件，计算每个月的平均销售额")
# Agent 会：
# 1. 生成 Python 代码读取CSV
# 2. 在 Sandbox 中安全执行
# 3. 返回执行结果
print(response)
