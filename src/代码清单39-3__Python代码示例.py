from typing import List, Dict, Optional
import asyncio

class ExecutionScheduler:
    """执行调度器"""

    def __init__(self, max_parallel: int = 3):
        self.max_parallel = max_parallel
        self.task_results: Dict[str, str] = {}

    def get_ready_tasks(
        self,
        tasks: List[SubTask]
    ) -> List[SubTask]:
        """获取当前可执行的任务"""
        completed_ids = set(self.task_results.keys())

        ready = []
        for task in tasks:
            if task.status == TaskStatus.COMPLETED:
                continue
            # 检查依赖是否都已完成
            deps_done = all(dep in completed_ids for dep in task.dependencies)
            if deps_done:
                ready.append(task)

        return ready

    async def execute_task(
        self,
        task: SubTask,
        executor_func
    ) -> tuple[str, str]:
        """执行单个任务"""
        try:
            result = await executor_func(task)
            self.task_results[task.task_id] = result
            task.status = TaskStatus.COMPLETED
            return task.task_id, result
        except Exception as e:
            task.status = TaskStatus.BLOCKED
            return task.task_id, f"执行失败: {str(e)}"

    async def execute_all(
        self,
        tasks: List[SubTask],
        executor_func
    ) -> Dict[str, str]:
        """执行所有任务"""
        while True:
            ready_tasks = self.get_ready_tasks(tasks)
            if not ready_tasks:
                break

            # 限制并行数
            batch = ready_tasks[:self.max_parallel]

            # 并行执行
            futures = [self.execute_task(t, executor_func) for t in batch]
            await asyncio.gather(*futures)

            # 检查是否全部完成
            if all(t.status == TaskStatus.COMPLETED for t in tasks):
                break

        return self.task_results

    def get_execution_plan(
        self,
        tasks: List[SubTask]
    ) -> List[List[str]]:
        """生成执行计划（哪些任务可以并行）"""
        plan = []
        remaining = tasks.copy()

        while remaining:
            ready = self.get_ready_tasks(remaining)
            if not ready:
                break
            plan.append([t.task_id for t in ready])
            for t in ready:
                remaining.remove(t)

        return plan