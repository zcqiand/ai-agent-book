from typing import Callable, Optional, Any
from dataclasses import dataclass
from enum import Enum
import asyncio
import traceback

class ErrorSeverity(str, Enum):
    """错误严重程度"""
    LOW = "low"         # 可忽略，自动恢复
    MEDIUM = "medium"   # 需要处理，但不影响主流程
    HIGH = "high"       # 需要立即处理
    CRITICAL = "critical"  # 系统级错误，需要人工介入

@dataclass
class ErrorContext:
    """错误上下文"""
    error: Exception
    agent_id: str
    workflow_id: Optional[str]
    task_id: Optional[str]
    severity: ErrorSeverity
    retry_count: int
    timestamp: str

class RetryPolicy:
    """重试策略"""

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_backoff: bool = True
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_backoff = exponential_backoff

    def get_delay(self, retry_count: int) -> float:
        """计算重试延迟"""
        if self.exponential_backoff:
            delay = self.base_delay * (2 ** retry_count)
        else:
            delay = self.base_delay
        return min(delay, self.max_delay)


class ErrorHandler:
    """Agent错误处理器"""

    def __init__(self, logger: AgentLogger):
        self.logger = logger
        self.retry_policies: dict = {}

    def with_retry(
        self,
        task_type: str,
        policy: RetryPolicy = None
    ):
        """装饰器：为函数添加重试逻辑"""
        if policy is None:
            policy = RetryPolicy()

        def decorator(func: Callable):
            async def wrapper(*args, **kwargs):
                last_error = None

                for attempt in range(policy.max_retries + 1):
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        last_error = e
                        self.logger.error(
                            f"Task {task_type} failed (attempt {attempt + 1})",
                            exc_info=True,
                            task_type=task_type,
                            attempt=attempt
                        )

                        if attempt < policy.max_retries:
                            delay = policy.get_delay(attempt)
                            await asyncio.sleep(delay)

                # 所有重试都失败
                raise last_error

            return wrapper
        return decorator

    def handle_error(self, context: ErrorContext) -> ErrorSeverity:
        """处理错误，返回严重程度"""
        error_type = type(context.error).__name__

        # 根据错误类型确定严重程度
        severity_map = {
            "TimeoutError": ErrorSeverity.MEDIUM,
            "RateLimitError": ErrorSeverity.MEDIUM,
            "AuthenticationError": ErrorSeverity.HIGH,
            "ValidationError": ErrorSeverity.LOW,
            "SystemError": ErrorSeverity.CRITICAL
        }

        severity = severity_map.get(error_type, ErrorSeverity.MEDIUM)

        # 记录错误
        self.logger.error(
            f"Error in {context.agent_id}: {str(context.error)}",
            workflow_id=context.workflow_id,
            task_id=context.task_id,
            severity=severity,
            error_type=error_type
        )

        return severity


class CircuitBreaker:
    """熔断器，防止故障扩散"""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        half_max_attempts: int = 3
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_max_attempts = half_max_attempts

        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.state = "closed"  # closed, open, half_open

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """执行函数，带熔断保护"""
        if self.state == "open":
            if self._should_attempt_reset():
                self.state = "half_open"
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        """成功回调"""
        self.failure_count = 0
        if self.state == "half_open":
            self.state = "closed"

    def _on_failure(self):
        """失败回调"""
        self.failure_count += 1
        self.last_failure_time = asyncio.get_event_loop().time()

        if self.failure_count >= self.failure_threshold:
            self.state = "open"

    def _should_attempt_reset(self) -> bool:
        """检查是否应该尝试重置"""
        if not self.last_failure_time:
            return True
        elapsed = asyncio.get_event_loop().time() - self.last_failure_time
        return elapsed >= self.recovery_timeout
