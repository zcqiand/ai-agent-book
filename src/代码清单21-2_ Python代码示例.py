from agents import Agent, handoff

# 定义专家 Agents
tech_expert = Agent(
    name="tech_expert",
    instructions="你是技术专家。回答技术问题，如果问题超出你的范围，返回'无法处理'。",
)

billing_expert = Agent(
    name="billing_expert",
    instructions="你是财务专家。回答账单、支付、退款问题。",
)

general_expert = Agent(
    name="general_expert",
    instructions="你是通用顾问。回答一般性问题。",
)

# Router Agent
router = Agent(
    name="router",
    instructions="""分析用户问题并转交给合适的专家：
    - 技术问题（故障、使用）→ tech_expert
    - 账单问题（支付、退款）→ billing_expert
    - 一般问题 → general_expert

    直接使用 handoff() 函数转交，不要自己回答。""",
    handoffs=[tech_expert, billing_expert, general_expert],
)

# 运行
result = router.run("我的产品坏了，无法启动")
# Router 分析意图 → 转交给 tech_expert → tech_expert 回答
