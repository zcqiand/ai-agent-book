class CrossValidatedEvaluator:
    """交叉验证评估器"""

    def __init__(self, llm):
        self.llm = llm
        self.dimension_evaluators = {
            "accuracy": AccuracyEvaluator(llm),
            "clarity": ClarityEvaluator(llm),
            "coherence": CoherenceEvaluator(llm)
        }

    def evaluate(self, content: str) -> dict:
        """执行交叉验证评估"""
        results = {}
        for dimension, evaluator in self.dimension_evaluators.items():
            # 同一内容多次评估
            scores = [evaluator.evaluate(content) for _ in range(3)]
            # 计算置信区间
            avg = sum(scores) / len(scores)
            variance = sum((s - avg) ** 2 for s in scores) / len(scores)
            results[dimension] = {
                "score": avg,
                "confidence": 1 - min(variance / 25, 1)  # 归一化置信度
            }
        return results
