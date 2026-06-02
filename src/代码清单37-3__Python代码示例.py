import asyncio
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor

class WorkerResult:
    """Worker执行结果"""
    def __init__(self, task_id: str, status: str, result: Any = None, error: Optional[str] = None):
        self.task_id = task_id
        self.status = status  # success, failed, timeout
        self.result = result
        self.error = error

class WorkerExecutionEngine:
    """Worker执行引擎"""

    def __init__(self, max_parallel: int = 5):
        self.max_parallel = max_parallel
        self.executor = ThreadPoolExecutor(max_workers=max_parallel)

    async def execute_task(self, subtask: SubTask, context: Dict) -> WorkerResult:
        """执行单个子任务"""
        worker = self._get_worker(subtask.assigned_worker)

        try:
            # 检查依赖是否满足
            for dep_id in subtask.dependencies:
                if not self._is_dependency_ready(dep_id, context):
                    return WorkerResult(
                        task_id=subtask.task_id,
                        status="failed",
                        error=f"依赖 {dep_id} 未完成"
                    )

            # 异步执行
            result = await asyncio.get_event_loop().run_in_executor(
                self.executor,
                worker.execute,
                subtask.description,
                context
            )

            # 更新上下文
            context[f"result_{subtask.task_id}"] = result

            return WorkerResult(task_id=subtask.task_id, status="success", result=result)

        except Exception as e:
            return WorkerResult(task_id=subtask.task_id, status="failed", error=str(e))

    async def execute_parallel(self, subtasks: List[SubTask], context: Dict) -> List[WorkerResult]:
        """并行执行多个子任务"""
        # 过滤出没有依赖的子任务
        ready_tasks = [t for t in subtasks if not t.dependencies]

        # 并行执行
        futures = [self.execute_task(task, context) for task in ready_tasks]
        results = await asyncio.gather(*futures)

        return results

    def _get_worker(self, worker_type: str):
        """获取对应类型的Worker"""
        # Worker注册表
        workers = {
            "research": ResearchWorker(),
            "order": OrderWorker(),
            "logistics": LogisticsWorker(),
            "analysis": AnalysisWorker(),
            "general": GeneralWorker()
        }
        return workers.get(worker_type, GeneralWorker())

    def _is_dependency_ready(self, dep_id: str, context: Dict) -> bool:
        """检查依赖是否已完成"""
        return f"result_{dep_id}" in context