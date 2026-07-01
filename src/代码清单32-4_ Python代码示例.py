from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.memory import ConversationSummaryMemory
from typing import Dict
import json

class EnterpriseChatSystem:
    """企业对话问答系统"""

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.embeddings = OpenAIEmbeddings()
        self.sessions: Dict[str, Dict] = {}
        self.vectorstores = {}

    def create_session(self, session_id: str, user_id: str):
        """创建会话"""
        self.sessions[session_id] = {
            "user_id": user_id,
            "created_at": "2026-05-09",
            "message_count": 0,
            "last_active": "2026-05-09"
        }

    def add_vectorstore(self, session_id: str, vs):
        """为会话添加知识库"""
        self.sessions[session_id]["vectorstore"] = vs

    def chat(self, session_id: str, message: str) -> str:
        """聊天"""
        if session_id not in self.sessions:
            return "会话不存在"

        session = self.sessions[session_id]
        session["message_count"] += 1

        # 简单实现：基于已有知识库回答
        if "vectorstore" in session:
            docs = session["vectorstore"].similarity_search(message, k=3)
            context = "\n".join([d.page_content for d in docs])
            prompt = f"基于以下内容回答：\n{context}\n\n问题：{message}"
        else:
            prompt = message

        response = self.llm.invoke(prompt)

        return response.content

    def get_session_info(self, session_id: str) -> dict:
        """获取会话信息"""
        if session_id not in self.sessions:
            return {"error": "会话不存在"}

        return {
            "session_id": session_id,
            "message_count": self.sessions[session_id]["message_count"],
            "user_id": self.sessions[session_id]["user_id"]
        }

# 使用
system = EnterpriseChatSystem()

# 创建会话
system.create_session("sess_001", "user_123")
system.add_vectorstore("sess_001", vectorstore)

# 对话
print(system.chat("sess_001", "年假政策是什么？"))
print(system.chat("sess_001", "有效期是多久？"))

# 查看会话信息
info = system.get_session_info("sess_001")
print(f"会话统计: {info}")
