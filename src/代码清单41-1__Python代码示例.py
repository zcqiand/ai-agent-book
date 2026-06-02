import logging
import json
from datetime import datetime
from typing import Any, Optional
from enum import Enum
import traceback

class LogLevel(str, Enum):
    """日志级别"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class AgentLogRecord:
    """Agent日志记录"""

    def __init__(
        self,
        level: LogLevel,
        agent_id: str,
        workflow_id: Optional[str],
        task_id: Optional[str],
        message: str,
        extra: dict = None
    ):
        self.timestamp = datetime.utcnow().isoformat()
        self.level = level
        self.agent_id = agent_id
        self.workflow_id = workflow_id
        self.task_id = task_id
        self.message = message
        self.extra = extra or {}

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "timestamp": self.timestamp,
            "level": self.level,
            "agent_id": self.agent_id,
            "workflow_id": self.workflow_id,
            "task_id": self.task_id,
            "message": self.message,
            **self.extra
        }

    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False)


class AgentLogger:
    """Agent日志记录器"""

    def __init__(self, agent_id: str, log_level: str = "INFO"):
        self.agent_id = agent_id
        self.logger = logging.getLogger(f"agent.{agent_id}")
        self.logger.setLevel(getattr(logging, log_level))

        # 添加JSON处理器
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(handler)

    def log(
        self,
        level: LogLevel,
        message: str,
        workflow_id: str = None,
        task_id: str = None,
        **extra
    ):
        """记录日志"""
        record = AgentLogRecord(
            level=level,
            agent_id=self.agent_id,
            workflow_id=workflow_id,
            task_id=task_id,
            message=message,
            extra=extra
        )
        self.logger.log(getattr(logging, level), record.to_json())

    def debug(self, message: str, **extra):
        self.log(LogLevel.DEBUG, message, **extra)

    def info(self, message: str, **extra):
        self.log(LogLevel.INFO, message, **extra)

    def warning(self, message: str, **extra):
        self.log(LogLevel.WARNING, message, **extra)

    def error(self, message: str, exc_info=None, **extra):
        if exc_info:
            extra["exception"] = traceback.format_exc()
        self.log(LogLevel.ERROR, message, **extra)