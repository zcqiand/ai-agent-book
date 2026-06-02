from functools import lru_cache

class CachedPlanningAgent(PlanningAgent):
    """带缓存的规划Agent"""

    def __init__(self, llm, executor_registry: dict, cache_size: int = 100):
        super().__init__(llm, executor_registry)
        self._analysis_cache = {}
        self._decompose_cache = {}

    def _get_cache_key(self, text: str) -> str:
        """生成缓存键"""
        import hashlib
        return hashlib.md5(text.encode()).hexdigest()

    async def process(self, user_goal: str) -> str:
        """处理用户目标（带缓存）"""
        # 检查缓存
        cache_key = self._get_cache_key(user_goal)

        if cache_key in self._analysis_cache:
            goal_analysis = self._analysis_cache[cache_key]
        else:
            goal_analysis = self.goal_analyzer.analyze(user_goal)
            self._analysis_cache[cache_key] = goal_analysis

        tasks = self.task_decomposer.decompose(user_goal, goal_analysis)
        # ... 执行部分保持不变