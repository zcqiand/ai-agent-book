from typing import Optional

class Optimizer:
    """优化器"""

    def __init__(self, llm):
        self.llm = llm

    def generate_initial(
        self,
        request: str,
        context: dict = None
    ) -> str:
        """生成初始内容"""
        prompt = f"""根据以下请求，生成高质量的内容。

请求：{request}

请生成完整、准确、有价值的内容。"""

        response = self.llm.invoke(prompt)
        return response.content

    def refine(
        self,
        original_content: str,
        evaluation: EvaluationResult,
        context: dict = None
    ) -> str:
        """根据评估反馈改进内容"""
        prompt = f"""请根据以下评估反馈，改进内容。

原始内容：
{original_content}

评估反馈：
- 总体评分：{evaluation.overall_score}/10
- 是否通过：{'是' if evaluation.passed else '否'}
- 改进建议：{evaluation.feedback}
- 发现的问题：{', '.join(evaluation.issues) if evaluation.issues else '无'}

请针对上述问题进行修改，生成改进后的版本。只输出修改后的内容，不要解释修改过程。"""

        response = self.llm.invoke(prompt)
        return response.content
