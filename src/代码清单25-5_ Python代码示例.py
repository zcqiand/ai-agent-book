from agents import Agent
from agents.hitl import pause

class DataManagementAgent:
    """数据管理助手（带审批）"""

    def __init__(self):
        self.agent = Agent(
            name="data_manager",
            instructions="""你是一个数据管理助手。
            执行以下操作前必须暂停等待批准：
            - 删除数据
            - 修改数据
            - 批量操作
            - 导出敏感数据

            暂停时清晰说明操作内容和风险。""",
        )

    def delete_data(self, table: str, record_id: str):
        """删除数据"""
        prompt = f"""
        准备删除数据：
        - 表：{table}
        - 记录ID：{record_id}

        评估删除风险并暂停等待批准。
        """

        return self.agent.run(prompt)

    def batch_operation(self, operation: str, scope: str):
        """批量操作"""
        prompt = f"""
        准备执行批量操作：
        - 操作：{operation}
        - 范围：{scope}

        由于是批量操作，风险较高，必须暂停等待批准。
        """

        return self.agent.run(prompt)
