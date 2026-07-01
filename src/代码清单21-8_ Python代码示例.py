from agents import Agent, handoff

# 1. 定义各级客服
auto_support = Agent(
    name="auto_support",
    instructions="""你是自动客服，处理常见问题：
    - 账户问题（密码重置、Profile修改）
    - 产品介绍
    - 常见FAQ

    如果无法处理，使用 handoff 转交给 tech_support。""",
    handoffs=["tech_support"]
)

tech_support = Agent(
    name="tech_support",
    instructions="""你是技术支持，处理技术问题：
    - 故障排查
    - 技术配置
    - 代码问题

    如果问题复杂需要人工介入，使用 handoff 转交给 human_support。""",
    handoffs=["human_support"]
)

human_support = Agent(
    name="human_support",
    instructions="你是人工客服，处理复杂问题。"
)

survey_agent = Agent(
    name="survey",
    instructions="""感谢使用我们的服务。请评价本次服务体验（1-5分）并简短说明。"""
)

# 2. 配置转交关系
auto_support.handoffs = [tech_support]
tech_support.handoffs = [human_support, survey_agent]  # 可以转交人工或直接结束

# 3. 运行入口
def run_customer_service(user_input: str):
    """运行客服系统"""
    return auto_support.run(user_input)

# 示例对话
# 用户：我的密码忘了
# auto_support：可以帮您重置密码...
# 用户：重置后还是登录不了
# auto_support → tech_support（handoff）
# tech_support：让我帮你排查...
# 用户：问题解决了
# tech_support → survey_agent（handoff）
# survey：请评价服务...
