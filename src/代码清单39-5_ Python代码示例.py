import asyncio
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class ResearchTask:
    """研究任务"""
    task_id: str
    query: str
    depth: str  # shallow, medium, deep
    status: str = "pending"
    results: Optional[List[str]] = None

class ResearchPlanner:
    """研究规划Agent"""

    def __init__(self, llm):
        self.llm = llm

    async def research(self, topic: str, depth: str = "medium") -> str:
        """执行研究任务"""
        # 分析研究主题
        sub_queries = await self._generate_sub_queries(topic, depth)

        # 并行执行子研究
        tasks = [
            ResearchTask(task_id=f"sub_{i}", query=q, depth=depth)
            for i, q in enumerate(sub_queries)
        ]

        results = await asyncio.gather(*[
            self._execute_research(t) for t in tasks
        ])

        # 聚合结果
        return self._aggregate(results)

    async def _generate_sub_queries(self, topic: str, depth: str) -> List[str]:
        """生成子查询"""
        depth_config = {
            "shallow": 2,
            "medium": 4,
            "deep": 8
        }
        num_queries = depth_config.get(depth, 4)

        prompt = f"""将以下研究主题分解为 {num_queries} 个子查询。

主题：{topic}

每个子查询应该：
- 覆盖主题的一个方面
- 具体且可独立搜索
- 互不重复

输出JSON数组格式的查询列表。"""

        response = self.llm.invoke(prompt)
        # 解析为查询列表
        return [f"{topic} - aspect {i+1}" for i in range(num_queries)]

    async def _execute_research(self, task: ResearchTask) -> str:
        """执行单个研究任务"""
        # 模拟研究过程
        await asyncio.sleep(0.1)
        return f"Research result for: {task.query}"

    def _aggregate(self, results: List[str]) -> str:
        """聚合研究结果"""
        combined = "\n".join(results)
        prompt = f"""基于以下研究结果，生成关于研究主题的综合报告。

研究结果：
{combined}

请整合这些结果，生成结构清晰、内容完整的报告。"""

        response = self.llm.invoke(prompt)
        return response.content

# 使用示例
async def demo():
    """演示研究规划Agent"""
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4")
    planner = ResearchPlanner(llm)

    topic = "人工智能在医疗诊断中的应用"
    result = await planner.research(topic, depth="medium")

    print(f"研究完成，结果长度：{len(result)} 字符")
    print(f"前200字预览：{result[:200]}...")

asyncio.run(demo())
