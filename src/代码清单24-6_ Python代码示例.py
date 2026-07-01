from agents import Agent
from agents.session import Session
import json

# 创建 Session
session = Session(agent=agent, session_id="export_demo")

session.run("我叫王五")
session.run("我是一名老师")

# 导出会话历史
exported = session.export()
print(exported)
# [
#   {"role": "user", "content": "我叫王五"},
#   {"role": "assistant", "content": "..."},
#   {"role": "user", "content": "我是一名老师"},
#   ...
# ]

# 保存为 JSON 文件
with open("conversation_backup.json", "w") as f:
    json.dump(exported, f, ensure_ascii=False, indent=2)

# 从备份恢复
with open("conversation_backup.json", "r") as f:
    backup = json.load(f)

session_restore = Session.from_backup(
    agent=agent,
    backup=backup
)
