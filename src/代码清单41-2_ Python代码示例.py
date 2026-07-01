from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry
from typing import Optional

class AgentMetrics:
    """Agent指标采集"""

    def __init__(self, agent_id: str, registry: CollectorRegistry = None):
        self.agent_id = agent_id
        self.registry = registry or CollectorRegistry()

        # 任务计数器
        self.task_counter = Counter(
            "agent_tasks_total",
            "Total number of tasks processed",
            ["agent_id", "task_type", "status"],
            registry=self.registry
        )

        # 任务延迟直方图
        self.task_duration = Histogram(
            "agent_task_duration_seconds",
            "Task processing duration",
            ["agent_id", "task_type"],
            registry=self.registry
        )

        # LLM调用计数器
        self.llm_calls = Counter(
            "agent_llm_calls_total",
            "Total number of LLM API calls",
            ["agent_id", "model", "status"],
            registry=self.registry
        )

        # Token使用量
        self.token_usage = Counter(
            "agent_token_usage_total",
            "Total token usage",
            ["agent_id", "model", "type"],
            registry=self.registry
        )

        # 当前活跃任务数
        self.active_tasks = Gauge(
            "agent_active_tasks",
            "Number of currently active tasks",
            ["agent_id"],
            registry=self.registry
        )

    def record_task_start(self, task_type: str):
        """记录任务开始"""
        self.active_tasks.labels(agent_id=self.agent_id).inc()

    def record_task_end(
        self,
        task_type: str,
        status: str,
        duration: float
    ):
        """记录任务结束"""
        self.active_tasks.labels(agent_id=self.agent_id).dec()
        self.task_counter.labels(
            agent_id=self.agent_id,
            task_type=task_type,
            status=status
        ).inc()
        self.task_duration.labels(
            agent_id=self.agent_id,
            task_type=task_type
        ).observe(duration)

    def record_llm_call(
        self,
        model: str,
        status: str,
        tokens: int = None
    ):
        """记录LLM调用"""
        self.llm_calls.labels(
            agent_id=self.agent_id,
            model=model,
            status=status
        ).inc()

        if tokens:
            self.token_usage.labels(
                agent_id=self.agent_id,
                model=model,
                type="total"
            ).inc(tokens)
