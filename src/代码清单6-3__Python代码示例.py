from agents import Agent, GuardrailFunctionOutput
from pydantic import BaseModel

class ContentSafetyOutput(BaseModel):
    is_safe: bool
    reason: str

def content_safety_check(ctx: GuardrailFunctionOutput) -> ContentSafetyOutput:
    """检查内容安全性"""
    text = ctx.output
    # 简化的安全检查逻辑
    blocked_words = ["暴力", "赌博", "诈骗"]
    for word in blocked_words:
        if word in text:
            return ContentSafetyOutput(is_safe=False, reason=f"包含敏感词：{word}")
    return ContentSafetyOutput(is_safe=True, reason="内容安全")

# 创建带护栏的 Agent
safe_agent = Agent(
    name="safe_assistant",
    instructions="你是一个有益的助手，用友好和专业的语气回答用户问题。",
    guardrails=[
        {
            "name": "content_safety",
            "description": "检查输出内容是否安全",
            "check": content_safety_check,
        }
    ],
)

# 运行
response = safe_agent.run("请介绍一下你们的公司")
print(response)