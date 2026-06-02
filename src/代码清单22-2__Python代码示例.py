from agents import Agent, handoff

# 1. 诊断 Agent
diagnostic_agent = Agent(
    name="diagnostic",
    instructions="""你是技术支持专家。你的职责是：
    1. 收集问题信息（错误信息、操作步骤、环境）
    2. 使用工具进行诊断
    3. 根据诊断结果转交给对应的处理 Agent

    诊断流程：
    - 询问用户问题现象
    - 要求提供错误日志（如果有）
    - 使用日志解析工具分析
    - 检索知识库是否有类似问题
    - 生成诊断报告

    如果无法诊断清楚，转交给人工支持。""",
    handoffs=["log_analyzer", "knowledge_base", "remote_support", "human_support"]
)

# 2. 日志分析 Agent
log_analyzer = Agent(
    name="log_analyzer",
    instructions="""解析错误日志，提取关键信息：
    - 错误类型和代码
    - 错误发生的时间和环境
    - 调用栈和上下文

    输出格式化的诊断报告。""",
)

# 3. 知识库检索 Agent
knowledge_base = Agent(
    name="knowledge_base",
    instructions="""在知识库中检索与用户问题相似的历史案例：
    - 使用关键词匹配
    - 使用语义相似度匹配
    - 返回最相关的解决方案

    如果找到相似问题，直接给出解决方案。
    如果没有找到，转交给诊断 Agent 继续排查。""",
)

# 4. 远程支持 Agent（需要用户授权）
remote_support = Agent(
    name="remote_support",
    instructions="""在用户授权下远程查看系统状态：
    - 检查配置是否正确
    - 查看服务运行状态
    - 收集诊断所需信息

    注意：必须获得用户明确授权才能进行远程操作。
    敏感操作需要用户确认。""",
)

# 5. 人工支持 Agent
human_support = Agent(
    name="human_support",
    instructions="转交给人工技术支持专家处理。",
    handoffs=["survey"]
)