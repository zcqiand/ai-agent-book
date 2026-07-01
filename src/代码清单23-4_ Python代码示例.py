from agents import Agent
from agents.sandbox import sandbox

# 创建文件处理 Agent
file_agent = Agent(
    name="file_agent",
    instructions="""你是一个文件处理助手。当用户请求处理文件时：
    1. 读取用户指定的文件
    2. 进行相应处理
    3. 将结果保存到输出文件
    4. 返回处理摘要

    注意：只能操作用户明确指定的文件，不能访问其他文件。""",
    tools=[sandbox]
)

# 处理文件
response = file_agent.run("请读取 data.csv 文件，计算其中 'price' 列的总和")
print(response)
