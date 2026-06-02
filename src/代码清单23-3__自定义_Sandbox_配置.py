from agents.sandbox import sandbox, SandboxConfiguration

# 自定义配置
config = SandboxConfiguration(
    timeout=30,           # 超时30秒
    memory_limit="256MB", # 内存限制256MB
    allowed_packages=["pandas", "numpy"],  # 允许的包
    blocked_modules=["os", "sys", "subprocess"],  # 禁止的模块
)

# 使用自定义配置
safe_agent = Agent(
    name="safe_agent",
    instructions="你是一个数据分析助手。",
    tools=[sandbox(config=config)]
)