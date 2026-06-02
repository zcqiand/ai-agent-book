from agents import Agent
from agents.session import Session, FileSessionStore

store = FileSessionStore("./sessions")
agent = Agent(name="assistant", instructions="你是一个有帮助的助手。")

# 创建 Session
session = Session(agent=agent, store=store, session_id="user_456")

# 对话
session.run("今天天气真好")
session.run("我心情也不错")

# 手动保存
session.save()

# 模拟服务重启
# ...

# 恢复 Session
session_restore = Session(
    agent=agent,
    store=store,
    session_id="user_456"
)

# 继续对话
response = session_restore.run("刚才我们聊什么了？")
print(response)  # 应该记得之前的对话