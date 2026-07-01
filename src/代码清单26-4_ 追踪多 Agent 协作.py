from agents import Agent, handoff
import agents.tracing as tracing

# 启用追踪
tracing.enable(project_name="multi-agent-tracing")

# 定义多个 Agent
router = Agent(
    name="router",
    instructions="分析问题并转交给合适的 Agent",
    handoffs=["tech_agent", "sales_agent"]
)

tech_agent = Agent(
    name="tech_agent",
    instructions="处理技术问题"
)

sales_agent = Agent(
    name="sales_agent",
    instructions="处理销售咨询"
)

# 运行
result = router.run("我有一个技术问题想咨询")

# 查看追踪
traces = tracing.list_traces(project_name="multi-agent-tracing")
for trace in traces[:5]:
    print(f"Trace: {trace.id}")
    print(f"Agent 数: {trace.agent_count}")
    print(f"总耗时: {trace.duration_ms}ms")
    print("-" * 50)
