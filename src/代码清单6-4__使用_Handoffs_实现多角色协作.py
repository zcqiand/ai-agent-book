from agents import Agent, handoff

# 定义各个角色的 Agent
triage_agent = Agent(
    name="triage",
    instructions="你是一个 triage（分诊）助手。分析用户的问题并转交给相应的专家：技术问题转给技术顾问，账单问题转给财务顾问，一般问题转给普通顾问。",
)

tech_advisor = Agent(
    name="tech_advisor",
    instructions="你是一个技术顾问。帮助用户解决技术问题，如产品使用、故障排除、功能咨询等。回答要专业但易懂。",
)

billing_advisor = Agent(
    name="billing_advisor",
    instructions="你是一个财务顾问。帮助用户解决账单、支付、退款等问题。要耐心和细致。",
)

general_advisor = Agent(
    name="general_advisor",
    instructions="你是一个通用顾问。回答一般性问题，提供信息咨询。",
)

# 定义 Handoffs
def route_to_tech(ctx):
    if "技术" in ctx.last_message.content or "故障" in ctx.last_message.content:
        return handoff(tech_advisor)

def route_to_billing(ctx):
    if "账单" in ctx.last_message.content or "支付" in ctx.last_message.content:
        return handoff(billing_advisor)

# 配置分流 Agent 的交接目标
triage_agent.handoffs = [tech_advisor, billing_advisor, general_advisor]

# 运行
response = triage_agent.run("我的产品坏了，无法启动")
print(response)