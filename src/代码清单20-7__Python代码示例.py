# Guardrails 方式：独立安全层
from agents import GuardrailFunctionOutput

def content_safety_check(output: GuardrailFunctionOutput) -> bool:
    """独立于 Prompt 的安全检查"""
    text = output.output
    # 检查逻辑
    if contains_harmful_content(text):
        return False
    return True

safe_agent = Agent(
    instructions="你是一个有帮助的助手",
    guardrails=[{"check": content_safety_check}]
)