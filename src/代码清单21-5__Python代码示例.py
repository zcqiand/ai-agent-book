from agents import Agent, handoff

# 场景：客服系统，根据问题严重程度转交给不同处理级别

tier1_support = Agent(name="tier1", instructions="处理简单问题")
tier2_support = Agent(name="tier2", instructions="处理中等复杂问题")
escalation = Agent(name="escalation", instructions="处理复杂问题，需要人工介入")

router = Agent(
    name="router",
    instructions="""分析问题并转交：

    如果问题简单且明确 → tier1_support
    如果问题中等复杂 → tier2_support
    如果问题复杂或敏感 → escalation

    转交时在 context 中说明问题严重程度和紧急程度。""",
    handoffs=[
        handoff(tier1_support, context={"tier": 1, "urgency": "normal"}),
        handoff(tier2_support, context={"tier": 2, "urgency": "elevated"}),
        handoff(escalation, context={"tier": 3, "urgency": "high"})
    ]
)