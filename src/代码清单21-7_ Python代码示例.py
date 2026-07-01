from agents import Agent, handoff

# 两个 Agent 互相转交（带退出条件）
agent_a = Agent(
    name="agent_a",
    instructions="""处理你的部分，然后转交给 agent_b。
    如果用户确认满意，返回'完成'。否则继续转交。""",
    handoffs=["agent_b"]
)

agent_b = Agent(
    name="agent_b",
    instructions="""处理你的部分，然后转交给 agent_a。
    如果用户确认满意，返回'完成'。否则继续转交。""",
    handoffs=["agent_a"]
)

# 实际应用中应该设置 max_turns 防止无限循环
# result = coordinator.run("...", max_turns=10)
