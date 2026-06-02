from agents import Agent
from agents.sandbox import sandbox

# 创建支持代码执行的 Agent
code_agent = Agent(
    name="code_agent",
    instructions="""你是一个编程助手。当用户请求数据分析或计算时：
    1. 生成 Python 代码
    2. 使用 sandbox 工具执行
    3. 解释执行结果

    可用库：pandas, numpy, matplotlib（用于可视化）""",
    tools=[sandbox]
)

# 示例：数学计算
response = code_agent.run("计算 1 到 100 之间所有质数的和")
print(response)