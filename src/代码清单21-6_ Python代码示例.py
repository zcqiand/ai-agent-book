from agents import Agent, handoff

# 信息收集 Agent
info_collector = Agent(
    name="info_collector",
    instructions="收集用户基本信息和问题描述。"
)

# 问题分析 Agent
problem_analyzer = Agent(
    name="problem_analyzer",
    instructions="""分析收集到的信息。

    收到的 context 包含：
    - user_id: 用户ID
    - user_tier: 用户等级
    - problem_category: 问题类别

    根据这些信息调整分析策略。"""
)

# 转交时携带上下文
info_collector.handoffs = [
    handoff(
        problem_analyzer,
        context={
            "user_id": "12345",
            "user_tier": "premium",
            "problem_category": "technical"
        }
    )
]

# 运行
result = info_collector.run("我的系统登录不了")
# 转交给 problem_analyzer 时携带了完整的上下文信息
