from agents import Agent
from agents.session import Session, FileSessionStore

# 使用文件存储
store = FileSessionStore(
    session_dir="./sessions",  # 存储目录
    max_sessions=100,          # 最大会话数
    auto_save=True             # 自动保存
)

agent = Agent(name="assistant", instructions="你是一个有帮助的助手。")

# 创建带持久化的 Session
session = Session(
    agent=agent,
    store=store,
    session_id="user_123"  # 指定会话ID
)

# 对话
session.run("我叫李明")
session.run("我是工程师")

# 保存（如果是 auto_save 则自动保存）
session.save()

# 之后可以恢复
session2 = Session(
    agent=agent,
    store=store,
    session_id="user_123"
)
response = session2.run("我叫什么？")  # 记住"李明"