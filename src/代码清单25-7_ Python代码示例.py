from agents import Agent
from agents.hitl import pause

class HumanInTheLoop客服系统:
    """带人机协作的客服系统"""

    def __init__(self):
        self.auto_agent = Agent(
            name="auto客服",
            instructions="处理常见问题，无法处理时转人工"
        )

        self.human_agent = Agent(
            name="人工客服",
            instructions="处理复杂问题和高风险操作"
        )

    def handle(self, issue: str, risk_level: str):
        """处理问题"""
        # 低风险问题自动处理
        if risk_level == "low":
            return self.auto_agent.run(issue)

        # 高风险问题暂停等待批准
        elif risk_level == "high":
            return self.high_risk_handling(issue)

        # 中等风险可选择转人工
        else:
            return self.medium_risk_handling(issue)

    def high_risk_handling(self, issue: str):
        """高风险问题处理"""
        prompt = f"""
        收到高风险操作请求：{issue}

        暂停等待人工批准。
        操作包括：退款、取消订单、修改用户数据等。
        """

        return self.human_agent.run(prompt)

    def medium_risk_handling(self, issue: str):
        """中等风险问题处理"""
        # AI 先尝试处理
        ai_result = self.auto_agent.run(issue)

        # 如果 AI 无法解决，提示转人工
        if "无法处理" in ai_result:
            return {
                "ai_result": ai_result,
                "human_needed": True,
                "transfer_to": "human_agent"
            }

        return ai_result
