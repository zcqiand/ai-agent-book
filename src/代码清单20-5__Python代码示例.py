from agents import Agent, handoff

# 定义 Agent
tech_expert = Agent(
    name="tech_expert",
    instructions="你是技术专家，回答技术问题"
)

billing_expert = Agent(
    name="billing_expert",
    instructions="你是财务专家，回答账单问题"
)

router = Agent(
    name="router",
    instructions="分析用户问题并转交给合适的专家",
    handoffs=[
        handoff(tech_expert, context={"source": "router"}),
        handoff(billing_expert, context={"source": "router"})
    ]
)

# 当 router 决定转交给 tech_expert 时：
# - tech_expert 收到完整对话历史
# - 额外收到 context={"source": "router"}
# - tech_expert 可以据此调整自己的行为