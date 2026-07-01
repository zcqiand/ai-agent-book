from agents import Agent
from agents.session import Session, FileSessionStore, SessionConfig
import json
from datetime import datetime

class ChatbotWithSessions:
    """带会话管理的聊天机器人"""

    def __init__(self, session_dir="./sessions"):
        self.agent = Agent(
            name="assistant",
            instructions="你是一个有帮助的助手。记住用户告诉你的重要信息。"
        )

        self.store = FileSessionStore(
            session_dir=session_dir,
            auto_save=True
        )

        self.config = SessionConfig(
            max_history=20,
            max_tokens=3000,
            summary_mode=True
        )

        self.sessions = {}  # 内存缓存

    def get_session(self, user_id: str) -> Session:
        """获取或创建 Session"""
        if user_id not in self.sessions:
            self.sessions[user_id] = Session(
                agent=self.agent,
                store=self.store,
                session_id=user_id,
                config=self.config
            )
        return self.sessions[user_id]

    def chat(self, user_id: str, message: str) -> str:
        """聊天"""
        session = self.get_session(user_id)
        response = session.run(message)
        return response

    def export_session(self, user_id: str, filepath: str):
        """导出会话"""
        session = self.get_session(user_id)
        exported = session.export()

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({
                "user_id": user_id,
                "exported_at": datetime.now().isoformat(),
                "messages": exported
            }, f, ensure_ascii=False, indent=2)

        return f"会话已导出到 {filepath}"

    def list_sessions(self):
        """列出所有会话"""
        return self.store.list_sessions()

    def delete_session(self, user_id: str):
        """删除会话"""
        self.store.delete_session(user_id)
        if user_id in self.sessions:
            del self.sessions[user_id]

# 使用示例
chatbot = ChatbotWithSessions()

# 用户1对话
chatbot.chat("user_1", "我叫张三")
chatbot.chat("user_1", "我是一名软件工程师")

# 用户2对话
chatbot.chat("user_2", "我叫李四")
chatbot.chat("user_2", "我是产品经理")

# 导出用户1的会话
chatbot.export_session("user_1", "zhangsan_chat.json")

# 列出所有会话
sessions = chatbot.list_sessions()
print(f"当前有 {len(sessions)} 个会话")
