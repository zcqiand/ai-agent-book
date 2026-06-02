from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from typing import List, Dict

class ConversationHistoryManager:
    """对话历史管理器"""

    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        self.sessions: Dict[str, List[Dict]] = {}

    def add_message(self, session_id: str, role: str, content: str):
        """添加消息"""
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append({
            "role": role,
            "content": content
        })

        # 自动截断过长的历史
        self._truncate_if_needed(session_id)

    def get_history(self, session_id: str) -> List[Dict]:
        """获取对话历史"""
        return self.sessions.get(session_id, [])

    def clear_history(self, session_id: str):
        """清空历史"""
        if session_id in self.sessions:
            self.sessions[session_id] = []

    def _truncate_if_needed(self, session_id: str):
        """截断过长的历史"""
        history = self.sessions[session_id]

        # 简单估算 token 数（中文字符约 2 token）
        total_chars = sum(len(m["content"]) for m in history)
        estimated_tokens = total_chars // 2

        while estimated_tokens > self.max_tokens and len(history) > 2:
            # 移除最早的消息
            removed = history.pop(0)
            total_chars -= len(removed["content"])
            estimated_tokens = total_chars // 2

    def get_context_window(self, session_id: str, window_size: int = 10) -> str:
        """获取最近 N 条消息作为上下文"""
        history = self.get_history(session_id)
        recent = history[-window_size:] if len(history) > window_size else history

        context = ""
        for msg in recent:
            role = "用户" if msg["role"] == "user" else "助手"
            context += f"{role}: {msg['content']}\n"

        return context

# 使用
manager = ConversationHistoryManager()

manager.add_message("session_1", "user", "公司的年假政策是什么？")
manager.add_message("session_1", "assistant", "根据员工手册，年假按工龄计算...")
manager.add_message("session_1", "user", "那加班调休呢？")

history = manager.get_history("session_1")
print(f"对话历史共 {len(history)} 条消息")