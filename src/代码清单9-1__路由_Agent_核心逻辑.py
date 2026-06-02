from agents import Agent, handoff

router = Agent(
    name="router",
    instructions="""你是一个智能路由助手。分析用户问题并转交给相应处理模块：
    - 知识查询类问题（公司政策、技术文档）→ rag_agent
    - 实时数据类问题（请假余额、审批状态）→ tool_agent
    - 一般性问题 → general_agent""",
    handoffs=[rag_agent, tool_agent, general_agent],
)