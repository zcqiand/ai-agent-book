from agents import Agent, handoff

class PaymentGuardrails:
    """支付安全护栏"""

    def check_payment(self, amount: float, user_id: str) -> bool:
        """检查支付是否安全"""
        # 大额支付需要额外验证
        if amount > 1000:
            return False  # 需要额外验证

        # 检查用户是否有不良记录
        if self.has_bad_record(user_id):
            return False

        return True

    def has_bad_record(self, user_id: str) -> bool:
        """检查用户是否有不良记录"""
        # 简化实现
        return False

guardrails = PaymentGuardrails()

# 支付 Agent
payment_agent = Agent(
    name="payment_agent",
    instructions="""你是支付专家。处理订单支付：
    - 验证支付信息
    - 检查安全护栏
    - 确认支付结果

    支付完成后通知用户。"""
)