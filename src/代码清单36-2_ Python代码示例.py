from enum import Enum
from typing import Optional
from pydantic import BaseModel

class MessageType(str, Enum):
    """消息类型枚举"""
    REQUEST = "request"           # 请求消息
    RESPONSE = "response"         # 响应消息
    BROADCAST = "broadcast"        # 广播消息
    ESCALATION = "escalation"      # 升级消息

class AgentMessage(BaseModel):
    """标准消息格式"""
    msg_type: MessageType
    sender: str                    # 发送者角色名
    receiver: Optional[str] = None  # 接收者，None表示广播
    content: dict                  # 消息内容
    conversation_id: str            # 会话ID，用于追踪
    timestamp: str                  # 时间戳

    def to_text(self) -> str:
        """序列化为可读文本"""
        return f"[{self.sender} -> {self.receiver or 'ALL'}]: {self.content}"
