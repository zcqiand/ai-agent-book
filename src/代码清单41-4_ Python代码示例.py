from prometheus_client import start_http_server
import logging
from typing import Dict

class MonitoringConfig:
    """监控配置"""

    def __init__(self, agent_id: str, port: int = 9090):
        self.agent_id = agent_id
        self.metrics_port = port
        self.logger = AgentLogger(agent_id)
        self.metrics = AgentMetrics(agent_id)
        self.error_handler = ErrorHandler(self.logger)

    def start_metrics_server(self):
        """启动Prometheus指标服务器"""
        start_http_server(self.metrics_port)
        self.logger.info(f"指标服务器启动在端口 {self.metrics_port}")

    def create_agent_wrapper(self, agent_func: callable):
        """创建带监控的Agent包装器"""
        async def monitored_agent(*args, **kwargs):
            import time

            # 记录开始
            task_type = getattr(agent_func, "__name__", "unknown")
            self.metrics.record_task_start(task_type)
            start_time = time.time()

            try:
                result = await agent_func(*args, **kwargs)
                duration = time.time() - start_time
                self.metrics.record_task_end(task_type, "success", duration)
                self.logger.info(f"Task {task_type} completed", duration=duration)
                return result

            except Exception as e:
                duration = time.time() - start_time
                self.metrics.record_task_end(task_type, "error", duration)
                self.logger.error(f"Task {task_type} failed", exc_info=True)
                raise

        return monitored_agent

    def add_llm_tracking(self, llm_call_func: callable):
        """添加LLM调用追踪"""
        async def tracked_llm_call(model: str, *args, **kwargs):
            import time
            try:
                start_time = time.time()
                result = await llm_call_func(model, *args, **kwargs)
                duration = time.time() - start_time

                # 记录成功调用
                self.metrics.record_llm_call(model, "success")
                self.logger.debug(
                    f"LLM call to {model} succeeded",
                    duration=duration
                )
                return result

            except Exception as e:
                self.metrics.record_llm_call(model, "error")
                self.logger.error(f"LLM call to {model} failed")
                raise

        return tracked_llm_call


# 使用示例
def setup_agent_monitoring(agent_id: str) -> MonitoringConfig:
    """为Agent设置监控"""
    config = MonitoringConfig(agent_id)

    # 启动指标服务器
    config.start_metrics_server()

    return config
