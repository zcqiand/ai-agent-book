from agents import Agent
from agents.hitl import pause

class EmailApprovalSystem:
    """带审批的邮件系统"""

    def __init__(self):
        self.agent = Agent(
            name="email_assistant",
            instructions="""你是一个邮件助手。帮助用户撰写邮件草稿。
            邮件草稿完成后必须暂停，等待用户批准才能发送。
            如果用户修改了内容，需要重新暂停等待批准。""",
        )

    def compose_email(self, to: str, subject: str, content: str):
        """撰写并发送邮件"""
        prompt = f"""
        请撰写一封邮件：
        - 收件人：{to}
        - 主题：{subject}
        - 内容：{content}

        撰写完成后，调用 pause() 等待用户批准。
        用户批准后，调用 send_email() 发送。
        """

        return self.agent.run(prompt)

    def approve(self, session_id: str):
        """批准发送"""
        # 获取会话
        session = self.get_session(session_id)
        # 继续执行
        return session.resume(action="approve")

    def reject(self, session_id: str, reason: str):
        """拒绝发送"""
        return f"邮件已取消，原因：{reason}"

# 使用
system = EmailApprovalSystem()
result = system.compose_email(
    to="team@company.com",
    subject="项目进度汇报",
    content="大家好，本周项目进度顺利..."
)

# 等待批准界面...
# 用户批准后
# system.approve(session_id)
