from typing import TypedDict, List
from pydantic import BaseModel
from enum import Enum

class ScoreLevel(str, Enum):
    """评分级别"""
    EXCELLENT = "excellent"  # 9-10分
    GOOD = "good"          # 7-8分
    ACCEPTABLE = "acceptable"  # 5-6分
    POOR = "poor"          # 3-4分
    FAIL = "fail"          # 0-2分

class EvaluationResult(BaseModel):
    """评估结果"""
    overall_score: float           # 总分 0-10
    passed: bool                    # 是否通过
    dimension_scores: dict          # 各维度分数
    feedback: str                   # 改进建议
    issues: List[str]               # 发现的问题列表

class Evaluator:
    """评估器"""

    def __init__(self, llm, dimension_weights: dict = None):
        self.llm = llm
        # 默认维度权重
        self.dimension_weights = dimension_weights or {
            "accuracy": 0.3,      # 准确性
            "completeness": 0.25, # 完整性
            "clarity": 0.2,       # 清晰度
            "relevance": 0.15,    # 相关性
            "format": 0.1         # 格式规范
        }

    def evaluate(
        self,
        content: str,
        criteria: str,
        context: dict = None
    ) -> EvaluationResult:
        """评估内容质量"""
        prompt = f"""请评估以下内容的质量。

评估标准：
{criteria}

待评估内容：
{content}

请从以下维度进行评分（每个维度0-10分）：
1. 准确性（accuracy）：内容是否正确无误
2. 完整性（completeness）：是否覆盖了所有必要信息
3. 清晰度（clarity）：表达是否清晰易懂
4. 相关性（relevance）：是否切题
5. 格式（format）：格式是否规范

同时给出：
- 总体评分（加权平均，0-10分）
- 是否通过（总体评分≥7为通过）
- 具体改进建议
- 发现的问题列表

输出JSON格式。"""

        response = self.llm.invoke(prompt)
        return self._parse_evaluation(response)

    def _parse_evaluation(self, response) -> EvaluationResult:
        """解析评估响应"""
        # 简化实现，实际应该解析JSON
        # 这里返回模拟结果
        return EvaluationResult(
            overall_score=7.5,
            passed=True,
            dimension_scores={
                "accuracy": 8.0,
                "completeness": 7.5,
                "clarity": 7.0,
                "relevance": 8.0,
                "format": 7.5
            },
            feedback="内容整体良好，建议加强逻辑衔接",
            issues=["第三段与第四段过渡不够自然", "部分数据引用需要更新"]
        )