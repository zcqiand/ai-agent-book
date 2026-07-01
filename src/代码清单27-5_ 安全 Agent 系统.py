from agents import Agent
from functools import wraps

class SecureAgentSystem:
    """安全的 Agent 系统"""

    def __init__(self):
        self.auth = Authenticator()
        self.authorizer = Authorizer()
        self.input_moderator = InputModerator()
        self.output_moderator = OutputModerator()
        self.audit_log = []

        self.agent = Agent(
            name="secure_assistant",
            instructions="你是一个有帮助的助手。"
        )

    def handle(self, api_key: str, user_input: str) -> dict:
        """处理用户请求"""

        # 1. 身份验证
        user_id = self.auth.verify(api_key)
        if not user_id:
            return {"error": "Unauthorized", "message": "身份验证失败"}

        # 2. 权限检查
        if not self.authorizer.check_permission(user_id, Permission.EXECUTE):
            return {"error": "Forbidden", "message": "权限不足"}

        # 3. 输入审核
        input_ok, reason = self.input_moderator.moderate(user_input)
        if not input_ok:
            self.audit_log.append({
                "user": user_id,
                "action": "input_rejected",
                "reason": reason
            })
            return {"error": "Rejected", "message": f"输入审核未通过: {reason}"}

        # 4. 执行 Agent
        response = self.agent.run(user_input)

        # 5. 输出审核
        output_ok, sensitive = self.output_moderator.moderate(response)
        if not output_ok:
            self.audit_log.append({
                "user": user_id,
                "action": "output_filtered",
                "sensitive": sensitive
            })
            # 过滤敏感内容
            response = self.filter_sensitive(response, sensitive)

        # 6. 记录审计日志
        self.audit_log.append({
            "user": user_id,
            "action": "query",
            "input": user_input,
            "output": response[:100]
        })

        return {"response": response}

    def filter_sensitive(self, text: str, sensitive: list) -> str:
        """过滤敏感内容"""
        for item in sensitive:
            text = text.replace(item, "[已过滤]")
        return text

    def get_audit_log(self, user_id: str = None):
        """获取审计日志"""
        if user_id:
            return [log for log in self.audit_log if log["user"] == user_id]
        return self.audit_log
