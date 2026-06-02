from agents import Agent, handoff

# 定义链上的各个 Agent
collector = Agent(
    name="collector",
    instructions="""收集用户信息：姓名、联系方式、问题类型。
    收集完成后使用 handoff() 转交给 processor。""",
    handoffs=["processor"]  # 字符串引用另一 Agent
)

processor = Agent(
    name="processor",
    instructions="""处理用户问题。根据问题类型：
    - 技术问题 → 转交给 tech_specialist
    - 投诉 → 转交给 complaint_handler
    - 其他 → 直接回答""",
    handoffs=["tech_specialist", "complaint_handler"]
)

tech_specialist = Agent(
    name="tech_specialist",
    instructions="处理技术问题，完成后返回结果给用户。"
)

complaint_handler = Agent(
    name="complaint_handler",
    instructions="处理投诉，完成后返回结果给用户。"
)

# 这种模式下，collector 收集信息 → processor 判断类型 →
# 转交给对应专家 → 专家返回结果