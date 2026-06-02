from agents import Agent, handoff
from typing import Optional

# 1. 定义各角色 Agent

# FAQ Agent
faq_agent = Agent(
    name="faq_agent",
    instructions="""你是公司产品的自动客服。处理以下类型的问题：
    - 账户相关（注册、登录、密码重置）
    - 产品介绍和功能咨询
    - 常见问题解答

    如果问题超出范围，使用 handoff 转交给技术支持或人工客服。
    回答要友好、专业。""",
    handoffs=["tech_support", "human_support"]
)

# 技术支持 Agent
tech_support = Agent(
    name="tech_support",
    instructions="""你是技术支持专家。处理以下类型的问题：
    - 产品故障排查
    - 技术配置指导
    - 错误信息解读

    如果问题无法解决，使用 handoff 转交给人工客服。
    需要时可以调用诊断工具。""",
    handoffs=["human_support"]
)

# 人工客服 Agent（实际生产中可能接入真人）
human_support = Agent(
    name="human_support",
    instructions="你是人工客服，处理复杂问题和特殊请求。",
    handoffs=["survey"]
)

# 满意度调查 Agent
survey_agent = Agent(
    name="survey",
    instructions="""感谢您使用我们的客服服务。请用1-5分评价本次服务，并简短说明原因。
    您的反馈将帮助我们改进服务。""",
)

# 2. 分流 Agent
classifier = Agent(
    name="classifier",
    instructions="""分析用户问题类型并转交给合适的客服：

    - 如果是常见问题（FAQ、账户、产品介绍）→ faq_agent
    - 如果是技术问题（故障、配置、报错）→ tech_support
    - 如果是投诉、复杂问题、需要人工判断 → human_support

    根据用户画像调整优先级：
    - 付费用户的问题优先处理
    - 紧急问题优先处理

    使用 handoff() 函数进行转交。""",
    handoffs=[faq_agent, tech_support, human_support]
)

# 3. 主入口
class CustomerServiceSystem:
    def __init__(self):
        self.classifier = classifier
        self.agents = {
            "faq": faq_agent,
            "tech": tech_support,
            "human": human_support
        }

    def handle(self, user_input: str, user_profile: dict = None) -> str:
        """处理用户请求"""
        # 根据用户画像调整分类器行为
        context = {}
        if user_profile:
            context["is_premium"] = user_profile.get("is_premium", False)
            context["user_tier"] = user_profile.get("tier", "free")

        # 启动分类器
        result = self.classifier.run(user_input)
        return result

# 4. 使用示例
css = CustomerServiceSystem()

# 普通用户
result1 = css.handle("我的密码忘了怎么办", {"tier": "free"})
# → faq_agent

# 付费用户
result2 = css.handle("系统报错500，请帮我看看", {"tier": "premium", "is_premium": True})
# → tech_support（付费用户优先技术支持）