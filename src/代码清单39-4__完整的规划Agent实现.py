from typing import Optional

class PlanningAgent:
    """规划Agent"""

    def __init__(self, llm, executor_registry: dict):
        self.goal_analyzer = GoalAnalyzer(llm)
        self.task_decomposer = TaskDecomposer(llm)
        self.execution_scheduler = ExecutionScheduler()
        self.executor_registry = executor_registry  # task_type -> executor

    async def process(self, user_goal: str) -> str:
        """处理用户目标"""
        context = {
            "original_goal": user_goal,
            "task_results": {}
        }

        # 第一步：目标分析
        goal_analysis = self.goal_analyzer.analyze(user_goal)
        context["analysis"] = goal_analysis

        # 第二步：任务分解
        tasks = self.task_decomposer.decompose(user_goal, goal_analysis)
        context["tasks"] = tasks

        # 生成执行计划
        plan = self.execution_scheduler.get_execution_plan(tasks)
        print(f"执行计划：{plan}")

        # 第三步：执行任务
        async def executor(task: SubTask) -> str:
            executor_func = self.executor_registry.get(task.task_id)
            if executor_func:
                return await executor_func(task)
            return f"Task {task.task_id} completed"

        task_results = await self.execution_scheduler.execute_all(tasks, executor)
        context["task_results"] = task_results

        # 第四步：结果整合
        final_result = self._aggregate_results(task_results, user_goal)

        return final_result

    def _aggregate_results(
        self,
        results: Dict[str, str],
        original_goal: str
    ) -> str:
        """聚合任务结果"""
        results_text = "\n".join([
            f"【{task_id}】{result}"
            for task_id, result in results.items()
        ])

        prompt = f"""根据以下任务执行结果，回答用户的原始目标。

原始目标：{original_goal}

任务执行结果：
{results_text}

请整合这些结果，给出完整的回答。"""

        response = self.llm.invoke(prompt)
        return response.content