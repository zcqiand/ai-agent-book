from agents import Agent, handoff

# 1. 定义各专家角色
tech_expert = Agent(
    name="tech_expert",
    instructions="""你是一个技术专家。处理产品使用、技术故障、功能咨询等问题。
    回答要专业、准确、易懂。如果无法解决，诚实地说明情况并建议其他解决途径。""",
)

billing_expert = Agent(
    name="billing_expert",
    instructions="""你是一个财务专家。处理账单、支付、退款、发票等问题。
    要耐心、细致，确保用户理解每一项费用。如果需要退款，按流程处理。""",
)

general_expert = Agent(
    name="general_expert",
    instructions="""你是一个通用顾问。回答一般性问题，提供产品信息、公司信息等。
    保持友好、专业的语气。""",
)

# 2. 定义满意度调查 Agent
survey_agent = Agent(
    name="survey",
    instructions="""感谢您使用我们的服务。请用1-5分评价本次服务体验（1分非常不满意，5分非常满意）。
    并简短说明原因。收集后记录用户反馈。""",
)

# 3. 定义分诊台 Agent
triage = Agent(
    name="triage",
    instructions="""你是一个客服分诊台。接收用户的问题，判断问题类型并转交给相应专家：
    - 技术问题（产品故障、使用问题）→ tech_expert
    - 账单问题（支付、退款、发票）→ billing_expert
    - 一般问题（产品信息、公司咨询）→ general_expert

    专家处理完成后，转交给 survey 进行满意度调查。
    所有转交都要使用 handoff 功能。""",
    handoffs=[tech_expert, billing_expert, general_expert, survey_agent],
)

# 运行示例
result = triage.run("我的账号登录不了了，提示密码错误")
print(result)