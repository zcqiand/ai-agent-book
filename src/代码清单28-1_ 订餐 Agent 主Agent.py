from agents import Agent, handoff

# 餐厅 Agent
restaurant_agent = Agent(
    name="restaurant_agent",
    instructions="""你是餐厅顾问。帮助用户：
    - 浏览餐厅列表和菜品
    - 根据用户口味推荐
    - 介绍餐厅和菜品的详细信息

    使用 handoff() 转交给订单 Agent 进行下单。"""
)

# 订单 Agent
order_agent = Agent(
    name="order_agent",
    instructions="""你是订单专家。帮助用户：
    - 创建订单
    - 查询订单状态
    - 修改订单（添加/删除菜品）
    - 取消订单

    下单前需要用户确认，使用 handoff() 转交给支付确认。"""
)

# 售后 Agent
support_agent = Agent(
    name="support_agent",
    instructions="""你是售后客服。帮助用户：
    - 处理投诉
    - 申请退款
    - 收集评价

    复杂问题转交给人工客服。""",
    handoffs=["human_support"]
)

# 主 Agent
main_agent = Agent(
    name="main_agent",
    instructions="""你是订餐助手。分析用户意图并转交给合适的 Agent：

    - 想看餐厅/菜品 → restaurant_agent
    - 想下单/查订单 → order_agent
    - 想投诉/退款 → support_agent

    使用 handoff() 进行转交。""",
    handoffs=[restaurant_agent, order_agent, support_agent]
)
