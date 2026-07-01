from agents import Agent
from agents.session import Session, SessionConfig

# Session 配置
config = SessionConfig(
    max_history=50,           # 最大历史消息数
    max_tokens=4000,          # 最大 Token 数
    summary_mode=True,        # 启用摘要模式
    auto_save_interval=30,    # 自动保存间隔（秒）
)

agent = Agent(name="assistant", instructions="你是一个有帮助的助手。")

session = Session(
    agent=agent,
    config=config
)

# 配置后，超过 max_history 的消息会被自动摘要
# 配置后，超过 max_tokens 的历史会被自动截断
