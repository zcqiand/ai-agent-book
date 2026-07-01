class IncrementalPlanner:
    """增量规划器"""

    def __init__(self, llm):
        self.llm = llm
        self.plan_history = []

    async def plan_incrementally(
        self,
        goal: str,
        context: dict
    ) -> str:
        """增量规划：每次只规划下一步"""
        # 基于历史和当前上下文，决定下一步
        next_action = await self._decide_next_action(goal, context)

        if self._is_goal_achieved(next_action, context):
            return self._aggregate_results()

        # 执行下一步
        result = await self._execute_action(next_action)
        self.plan_history.append((next_action, result))

        # 递归规划下一步
        return await self.plan_incrementally(goal, {**context, **result})
