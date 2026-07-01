class OutputModerator:
    """输出内容审核"""

    def __init__(self):
        self.sensitive_patterns = [
            r"\d{3}-\d{2}-\d{4}",  # 社保号
            r"\d{16}",            # 信用卡号
            r"api[_-]?key.*=.*[a-zA-Z0-9]",  # API Key
        ]

    def moderate(self, text: str) -> tuple[bool, list]:
        """审核输出，返回 (是否通过, 敏感内容列表)"""
        found = []

        for pattern in self.sensitive_patterns:
            matches = re.findall(pattern, text)
            if matches:
                found.extend(matches)

        if found:
            return False, found

        return True, []

moderator = OutputModerator()

# 测试
result = moderator.moderate("您的订单号是12345")
print(f"结果: {result}")  # (True, [])

result = moderator.moderate("您的密码是abc123api_key=xyz")
print(f"结果: {result}")  # (False, ['abc123api_key=xyz'])
