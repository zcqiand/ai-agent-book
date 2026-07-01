import asyncio
from dataclasses import dataclass, field
from typing import List, Optional, Callable
from enum import Enum
import time

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"

@dataclass
class AdaptiveTask:
    """自适应任务"""
    task_id: str
    description: str
    estimated_duration: float  # 预估时长（秒）
    actual_duration: Optional[float] = None
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    error: Optional[str] = None

class AdaptiveDecomposer:
    """自适应任务分解系统"""

    def __init__(self, max_execution_time: float = 30.0):
        self.max_execution_time = max_execution_time
        self.tasks: List[AdaptiveTask] = []

    def analyze_and_decompose(self, query: str) -> List[AdaptiveTask]:
        """分析并分解任务"""
        # 简化版分析逻辑
        complexity_hints = self._detect_complexity(query)

        if complexity_hints["level"] == "low":
            return [AdaptiveTask(
                task_id="simple_1",
                description=query,
                estimated_duration=5.0
            )]
        elif complexity_hints["level"] == "medium":
            return self._decompose_medium(query)
        else:
            return self._decompose_high(query)

    def _detect_complexity(self, query: str) -> dict:
        """检测任务复杂度"""
        # 简化版检测逻辑
        complexity_indicators = {
            "high": ["分析", "比较", "评估", "详细", "全面", "研究", "调查", "评估"],
            "medium": ["查询", "查找", "获取", "了解", "查看", "确认"],
            "low": ["问候", "谢谢", "再见", "你好", "帮忙"]
        }

        text = query.lower()
        scores = {"low": 0, "medium": 0, "high": 0}

        for level, keywords in complexity_indicators.items():
            for keyword in keywords:
                if keyword in text:
                    scores[level] += 1

        max_level = max(scores, key=scores.get)
        return {"level": max_level, "scores": scores}

    def _decompose_medium(self, query: str) -> List[AdaptiveTask]:
        """分解中等复杂度任务"""
        return [
            AdaptiveTask(
                task_id="med_1",
                description=f"处理: {query}",
                estimated_duration=10.0
            )
        ]

    def _decompose_high(self, query: str) -> List[AdaptiveTask]:
        """分解高复杂度任务"""
        return [
            AdaptiveTask(
                task_id="high_1",
                description=f"信息收集: {query}",
                estimated_duration=8.0
            ),
            AdaptiveTask(
                task_id="high_2",
                description=f"分析处理: {query}",
                estimated_duration=12.0
            ),
            AdaptiveTask(
                task_id="high_3",
                description=f"结果汇总: {query}",
                estimated_duration=5.0
            )
        ]

async def execute_with_timeout(
    task: AdaptiveTask,
    executor_func: Callable,
    timeout: float
) -> AdaptiveTask:
    """带超时控制的执行"""
    start_time = time.time()

    try:
        result = await asyncio.wait_for(
            executor_func(task),
            timeout=timeout
        )
        task.result = result
        task.status = TaskStatus.COMPLETED
    except asyncio.TimeoutError:
        task.status = TaskStatus.TIMEOUT
        task.error = f"执行超时（>{timeout}秒）"
    except Exception as e:
        task.status = TaskStatus.FAILED
        task.error = str(e)
    finally:
        task.actual_duration = time.time() - start_time

    return task

# 使用示例
async def demo():
    """演示自适应任务分解"""
    decomposer = AdaptiveDecomposer(max_execution_time=30.0)

    # 测试不同复杂度
    queries = [
        "你好",
        "帮我查一下订单A123的状态",
        "帮我分析一下公司的财务状况，包括营收、成本、利润趋势"
    ]

    for query in queries:
        print(f"\n任务: {query}")
        tasks = decomposer.analyze_and_decompose(query)
        print(f"分解为 {len(tasks)} 个子任务:")
        for task in tasks:
            print(f"  - {task.task_id}: {task.description} (预估{task.estimated_duration}秒)")

asyncio.run(demo())
