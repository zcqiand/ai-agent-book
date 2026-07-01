from agents import Agent
from agents.hitl import pause

class FinanceApprovalWorkflow:
    """财务审批工作流"""

    def __init__(self):
        self.agent = Agent(
            name="finance_assistant",
            instructions="""你是一个财务助手。处理报销、付款等财务请求。

            分级审批规则：
            - 1000元以下：AI 直接处理
            - 1000-10000元：主管审批
            - 10000元以上：部门经理+财务双重审批

            对于需要审批的请求，调用 pause() 并清晰说明：
            - 申请人信息
            - 金额和类型
            - 预算归属
            - 风险提示""",
        )

    def process_expense(self, employee: str, amount: float, description: str):
        """处理报销"""
        if amount <= 1000:
            # 小额直接处理
            return self.execute_expense(employee, amount, description)
        else:
            # 需要审批
            prompt = f"""
            收到报销申请：
            - 申请人：{employee}
            - 金额：{amount}元
            - 说明：{description}

            请按照分级审批规则处理。"""

            return self.agent.run(prompt)
