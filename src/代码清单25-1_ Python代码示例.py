from agents import Agent
from agents.hitl import pause, approve

# 创建需要审批的 Agent
email_agent = Agent(
    name="email_agent",
    instructions="""你是一个邮件助手。帮助用户撰写和发送邮件。

    重要规则：
    - 在发送任何邮件之前，必须调用 pause() 暂停
    - 等待用户批准后才能发送
    - 如果用户否决，说明原因并等待调整""",
)

# 定义发送邮件的工具
@tool
def send_email(to: str, subject: str, body: str):
    """发送邮件"""
    # 实际发送逻辑
    return f"邮件已发送给 {to}"

# 使用
response = email_agent.run(
    "给团队发送会议提醒邮件，主题是'项目进度会议'，时间是明天下午3点"
)
# Agent 会暂停，等待用户批准后才真正发送
