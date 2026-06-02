from agents import Agent
import agents.tracing as tracing

# 创建带追踪的 Agent
agent = Agent(
    name="assistant",
    instructions="你是一个有帮助的助手。",
    tracing=True  # 显式启用追踪
)

# 添加自定义追踪事件
@tracing.trace("custom_step")
def custom_processing(data):
    """自定义处理步骤"""
    return process(data)

# 运行
result = agent.run("请帮我处理数据")