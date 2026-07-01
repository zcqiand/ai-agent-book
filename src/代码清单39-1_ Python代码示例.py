from typing import TypedDict, List, Optional
from pydantic import BaseModel
from enum import Enum

class GoalClarity(str, Enum):
    """目标清晰度"""
    CLEAR = "clear"       # 目标明确
    PARTIAL = "partial"  # 部分明确
    FUZZY = "fuzzy"      # 目标模糊

class Constraint(BaseModel):
    """约束条件"""
    name: str
    description: str
    type: str  # budget, time, quality, scope

class GoalAnalysis(BaseModel):
    """目标分析结果"""
    clarity: GoalClarity
    scope: List[str]           # 目标覆盖的范围
    constraints: List[Constraint]  # 约束条件
    success_criteria: str      # 成功标准
    potential_issues: List[str]  # 潜在问题

class GoalAnalyzer:
    """目标分析器"""

    def __init__(self, llm):
        self.llm = llm

    def analyze(self, user_goal: str) -> GoalAnalysis:
        """分析用户目标"""
        prompt = f"""分析以下用户目标，返回结构化的分析结果。

用户目标：{user_goal}

请从以下维度进行分析：
1. 目标清晰度（clear/partial/fuzzy）
2. 目标覆盖的范围（需要涉及哪些方面）
3. 约束条件（如有）
4. 成功标准（怎样算完成）
5. 潜在问题（可能遇到哪些困难）

输出JSON格式。"""

        response = self.llm.invoke(prompt)
        return self._parse_response(response)

    def _parse_response(self, response) -> GoalAnalysis:
        """解析LLM响应"""
        # 简化实现，实际应该解析JSON
        return GoalAnalysis(
            clarity=GoalClarity.PARTIAL,
            scope=["信息收集", "对比分析", "报告生成"],
            constraints=[],
            success_criteria="生成完整的对比分析报告",
            potential_issues=["信息可能不完整", "竞品范围可能需要调整"]
        )
