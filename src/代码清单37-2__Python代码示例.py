from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class SubTask:
    """子任务定义"""
    task_id: str
    description: str
    assigned_worker: str
    dependencies: List[str]  # 依赖的其他子任务ID
    priority: int           # 优先级（数字越小越高）

class DynamicDecomposer:
    """动态任务分解器"""

    def __init__(self, worker_registry: Dict[str, Any]):
        self.worker_registry = worker_registry  # 可用Worker注册表
        self.llm = None  # 注入LLM

    def decompose(self, task_analysis: TaskAnalysis, user_query: str) -> List[SubTask]:
        """根据任务分析动态分解"""
        if task_analysis.complexity == ComplexityLevel.SIMPLE:
            # 简单任务直接返回，无需分解
            return [SubTask(
                task_id="direct",
                description=user_query,
                assigned_worker="general",
                dependencies=[],
                priority=1
            )]

        # 中等和复杂任务进行分解
        subtasks = self._generate_subtasks(task_analysis, user_query)

        # 添加依赖关系
        subtasks = self._resolve_dependencies(subtasks)

        return subtasks

    def _generate_subtasks(self, analysis: TaskAnalysis, query: str) -> List[SubTask]:
        """生成子任务列表"""
        # 提示LLM根据任务类型生成合适的子任务
        prompt = f"""根据以下任务分析，为复杂任务生成子任务列表。

任务类型：{analysis.task_type}
关键实体：{', '.join(analysis.key_entities) if analysis.key_entities else '无'}
用户请求：{query}

可用Worker类型：
- research: 研究分析Worker
- order: 订单处理Worker
- logistics: 物流Worker
- analysis: 数据分析Worker
- general: 通用处理Worker

请生成 {analysis.estimated_subtasks} 个子任务，每个子任务包含：
- task_id: 任务ID（如 task_1, task_2）
- description: 任务描述
- assigned_worker: 分配的Worker类型

输出JSON数组格式。"""

        # 实际调用LLM生成
        # 返回 SubTask 列表
        return []

    def _resolve_dependencies(self, subtasks: List[SubTask]) -> List[SubTask]:
        """解析子任务间的依赖关系"""
        # 某些子任务可能依赖其他子任务的结果
        # 例如：聚合任务必须最后执行
        for i, task in enumerate(subtasks):
            if task.assigned_worker == "aggregator":
                # 聚合任务依赖所有其他任务
                task.dependencies = [t.task_id for t in subtasks if t.task_id != task.task_id]

        return subtasks