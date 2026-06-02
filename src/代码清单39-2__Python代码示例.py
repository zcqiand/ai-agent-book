from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class TaskPriority(str, Enum):
    """任务优先级"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class TaskStatus(str, Enum):
    """任务状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"

@dataclass
class SubTask:
    """子任务定义"""
    task_id: str
    title: str
    description: str
    priority: TaskPriority
    dependencies: List[str]  # 依赖的任务ID列表
    status: TaskStatus = TaskStatus.PENDING
    estimated_duration: Optional[float] = None  # 预估时长（分钟）
    result: Optional[str] = None

class TaskDecomposer:
    """任务分解器"""

    def __init__(self, llm):
        self.llm = llm

    def decompose(
        self,
        goal: str,
        goal_analysis: GoalAnalysis
    ) -> List[SubTask]:
        """将目标分解为子任务"""
        prompt = f"""根据以下目标分析，将任务分解为可执行的子任务。

用户目标：{goal}

目标范围：{', '.join(goal_analysis.scope)}
成功标准：{goal_analysis.success_criteria}
潜在问题：{', '.join(goal_analysis.potential_issues)}

请生成子任务列表，每个子任务包含：
- task_id: 任务ID（如 task_1, task_2）
- title: 任务标题（简洁）
- description: 任务详细描述
- priority: 优先级（high/medium/low）
- dependencies: 依赖的其他任务ID列表（无依赖则为空列表）
- estimated_duration: 预估完成时长（分钟）

请确保：
1. 子任务是原子性的，可以独立执行
2. 依赖关系正确，无循环依赖
3. 覆盖目标的所有范围

输出JSON数组格式。"""

        response = self.llm.invoke(prompt)
        return self._parse_response(response)

    def _parse_response(self, response) -> List[SubTask]:
        """解析分解结果"""
        # 简化实现
        return [
            SubTask(
                task_id="task_1",
                title="收集竞品信息",
                description="搜索并收集主要竞争对手的基本信息",
                priority=TaskPriority.HIGH,
                dependencies=[],
                estimated_duration=10
            ),
            SubTask(
                task_id="task_2",
                title="对比分析",
                description="从多个维度对比各竞品的优劣势",
                priority=TaskPriority.HIGH,
                dependencies=["task_1"],
                estimated_duration=15
            ),
            SubTask(
                task_id="task_3",
                title="生成报告",
                description="整合分析结果，生成完整的对比分析报告",
                priority=TaskPriority.MEDIUM,
                dependencies=["task_2"],
                estimated_duration=10
            )
        ]