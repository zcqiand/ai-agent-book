from agents import Agent
from agents.hitl import pause, intervene

# 创建需要干预的 Agent
content_agent = Agent(
    name="content_agent",
    instructions="""你是一个内容审核助手。审核用户生成的内容。

    发现问题时：
    1. 调用 pause() 暂停
    2. 标记问题类型（违规/疑似违规/待确认）
    3. 等待人工干预

    人工干预选项：
    - 批准：内容通过
    - 修改：指出需要修改的部分
    - 拒绝：内容违规，拒绝发布""",
)

# 审核内容
def review_content(content: str):
    """审核内容"""
    result = content_agent.run(f"审核以下内容：{content}")

    # 如果有干预请求，等待处理
    if result.needs_intervention:
        print(f"内容需要人工干预，类型：{result.issue_type}")
        print(f"内容预览：{content[:100]}...")

        # 人工处理
        # decision = human_review(result)
        # return decision

    return result
