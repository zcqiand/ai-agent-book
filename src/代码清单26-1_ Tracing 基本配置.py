from agents import Agent
import agents.tracing as tracing

# 启用 Tracing
tracing.enable(
    project_name="my-agent-project",  # 项目名称
    endpoint="https://api.tracing.ai"   # Tracing 服务端点
)

# 或者使用环境变量
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_PROJECT=my-agent-project

agent = Agent(
    name="assistant",
    instructions="你是一个有帮助的助手。"
)

# 运行 - 自动被追踪
result = agent.run("你好")
