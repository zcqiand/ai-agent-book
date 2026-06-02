from agents import Agent

# 创建 Agent
agent = Agent(
    name="assistant",
    instructions="你是一个有帮助的助手",
    tools=[],
)

# Agent 运行于一个 run() 方法中
# 内部执行：
# 1. 接收输入 (run input)
# 2. 生成 LLM 调用 (generate)
# 3. 处理工具调用 (execute tools)
# 4. 决定是否结束或继续 (loop until done)
result = agent.run("你好")

# 每个 run() 是独立的
# 但可以通过 handoffs 共享上下文