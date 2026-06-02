from typing import Dict, Any, Optional

class Orchestrator:
    """完整的Orchestrator-Workers系统"""

    def __init__(self, config: Dict[str, Any]):
        self.task_analyzer = TaskAnalyzer(config["llm"])
        self.decomposer = DynamicDecomposer(config["worker_registry"])
        self.execution_engine = WorkerExecutionEngine()
        self.result_aggregator = ResultAggregator(config["llm"])

    async def process(self, user_query: str) -> str:
        """处理用户请求的完整流程"""
        context = {
            "original_query": user_query,
            "subtask_results": {},
            "metadata": {}
        }

        # 第一步：任务分析
        task_analysis = self.task_analyzer.analyze(user_query)
        context["analysis"] = task_analysis

        # 第二步：动态分解
        subtasks = self.decomposer.decompose(task_analysis, user_query)
        context["subtasks"] = subtasks

        # 第三步：按依赖顺序执行
        results = await self._execute_with_dependencies(subtasks, context)

        # 第四步：结果聚合
        final_response = self.result_aggregator.aggregate(
            query=user_query,
            subtask_results=results,
            context=context
        )

        return final_response

    async def _execute_with_dependencies(
        self,
        subtasks: List[SubTask],
        context: Dict
    ) -> List[WorkerResult]:
        """按依赖顺序执行子任务"""
        completed = []
        remaining = subtasks.copy()

        while remaining:
            # 找出所有依赖都已完成的子任务
            ready = [
                t for t in remaining
                if all(dep in [r.task_id for r in completed] for dep in t.dependencies)
            ]

            if not ready:
                # 无法继续执行，存在循环依赖
                break

            # 并行执行准备好的子任务
            results = await self.execution_engine.execute_parallel(ready, context)
            completed.extend(results)

            # 移除已完成的
            remaining = [t for t in remaining if t not in ready]

        return completed


class ResultAggregator:
    """结果聚合器"""

    def __init__(self, llm):
        self.llm = llm

    def aggregate(
        self,
        query: str,
        subtask_results: List[WorkerResult],
        context: Dict
    ) -> str:
        """聚合子任务结果生成最终回答"""
        # 过滤成功的结果
        successful = [r for r in subtask_results if r.status == "success"]

        if not successful:
            return "抱歉，处理过程中遇到了问题，请稍后重试。"

        # 构建结果摘要
        results_summary = "\n".join([
            f"【{r.task_id}】{r.result}"
            for r in successful
        ])

        prompt = f"""基于以下子任务结果，回答用户的原始问题。

原始问题：{query}

子任务执行结果：
{results_summary}

请综合分析这些结果，给出完整、连贯的回答。如果某些子任务失败，请在回答中说明。
回答应该直接面向用户，不要提及内部处理过程。"""

        response = self.llm.invoke(prompt)
        return response.content