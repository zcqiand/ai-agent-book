class ReflectiveOptimizer(Optimizer):
    """具备自我反思能力的优化器"""

    def __init__(self, llm):
        super().__init__(llm)

    def reflective_refine(
        self,
        original_content: str,
        evaluation: EvaluationResult,
        context: dict = None
    ) -> str:
        """反思式改进：不仅修改问题，还要理解问题根源"""
        # 第一步：理解问题根源
        root_cause_prompt = f"""分析以下内容存在问题的根本原因。

内容：
{original_content}

评估反馈：
{evaluation.feedback}

请深入分析，不要只看到表面问题，而是理解问题的本质原因。
例如：「逻辑断层」可能是因为「没有建立因果关系」，而「没有建立因果关系」可能是因为「缺少过渡句」。

输出JSON格式，包含：
- surface_issues: 表面问题列表
- root_causes: 根本原因列表
- recommended_approach: 推荐的修改方法"""

        analysis = self.llm.invoke(root_cause_prompt)
        # 解析分析结果...

        # 第二步：基于根源分析生成改进
        refine_prompt = f"""请根据以下深入分析，改进内容。

原始内容：
{original_content}

根本原因分析：
- 表面问题：{analysis.get('surface_issues', [])}
- 根本原因：{analysis.get('root_causes', [])}
- 推荐方法：{analysis.get('recommended_approach', '')}

请针对根本原因进行系统性修改，生成改进后的内容。"""

        response = self.llm.invoke(refine_prompt)
        return response.content
