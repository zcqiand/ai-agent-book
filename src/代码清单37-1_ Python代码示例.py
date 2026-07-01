from typing import TypedDict, List, Optional
from enum import Enum
from pydantic import BaseModel

class ComplexityLevel(str, Enum):
    """复杂度级别"""
    SIMPLE = "simple"      # 简单任务，单轮处理
    MODERATE = "moderate" # 中等复杂度，需多步处理
    COMPLEX = "complex"   # 复杂任务，需大量子任务

class TaskAnalysis(BaseModel):
    """任务分析结果"""
    complexity: ComplexityLevel
    task_type: str                    # 任务类型：research/order/analysis/etc
    key_entities: List[str]          # 关键实体
    estimated_subtasks: int          # 预估子任务数量
    requires_external_data: bool     # 是否需要外部数据
    special_requirements: List[str]  # 特殊需求

class TaskAnalyzer:
    """任务分析器"""

    def __init__(self, llm):
        self.llm = llm

    def analyze(self, user_query: str) -> TaskAnalysis:
        """分析用户任务"""
        prompt = f"""分析以下用户任务，返回结构化的分析结果。

用户任务：{user_query}

请从以下维度进行分析：
1. 复杂度级别（simple/moderate/complex）
2. 任务类型（如 research、order、analysis、general）
3. 关键实体（人名、地点、订单号、产品名等）
4. 预估需要的子任务数量（1-10）
5. 是否需要访问外部数据或API
6. 任何特殊需求

直接输出分析结果，不需要额外解释。"""

        response = self.llm.invoke(prompt)
        # 解析响应为 TaskAnalysis 对象
        # 实际实现中应该用 JSON 解析
        return self._parse_response(response)

    def _parse_response(self, response) -> TaskAnalysis:
        """解析LLM响应"""
        # 简化实现，实际应该解析结构化输出
        text = response.content.lower()

        if any(word in text for word in ["简单", "simple", "一步", "快速"]):
            complexity = ComplexityLevel.SIMPLE
        elif any(word in text for word in ["复杂", "complex", "多个", "详细"]):
            complexity = ComplexityLevel.COMPLEX
        else:
            complexity = ComplexityLevel.MODERATE

        return TaskAnalysis(
            complexity=complexity,
            task_type="general",
            key_entities=[],
            estimated_subtasks=3,
            requires_external_data="api" in text or "数据" in text,
            special_requirements=[]
        )
