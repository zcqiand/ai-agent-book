from dataclasses import dataclass
from typing import Optional, List

@dataclass
class IterationRecord:
    """迭代记录"""
    iteration: int
    content: str
    score: float
    feedback: str
    passed: bool

class IterativeOptimizer:
    """迭代优化控制器"""

    def __init__(
        self,
        optimizer: Optimizer,
        evaluator: Evaluator,
        max_iterations: int = 5,
        min_score: float = 7.0,
        min_improvement: float = 0.5
    ):
        self.optimizer = optimizer
        self.evaluator = evaluator
        self.max_iterations = max_iterations
        self.min_score = min_score
        self.min_improvement = min_improvement

        self.history: List[IterationRecord] = []

    def optimize(
        self,
        request: str,
        criteria: str,
        context: dict = None
    ) -> tuple[str, List[IterationRecord]]:
        """执行迭代优化"""
        # 第一轮：生成初始内容
        current_content = self.optimizer.generate_initial(request, context)
        evaluation = self.evaluator.evaluate(current_content, criteria, context)

        self.history.append(IterationRecord(
            iteration=1,
            content=current_content,
            score=evaluation.overall_score,
            feedback=evaluation.feedback,
            passed=evaluation.passed
        ))

        # 检查是否直接通过
        if evaluation.passed:
            return current_content, self.history

        # 迭代优化
        for i in range(2, self.max_iterations + 1):
            # 生成改进版本
            current_content = self.optimizer.refine(
                current_content,
                evaluation,
                context
            )

            # 评估改进版本
            evaluation = self.evaluator.evaluate(current_content, criteria, context)

            self.history.append(IterationRecord(
                iteration=i,
                content=current_content,
                score=evaluation.overall_score,
                feedback=evaluation.feedback,
                passed=evaluation.passed
            ))

            # 检查质量是否达标
            if evaluation.passed:
                break

            # 检查改进幅度
            last_score = self.history[-2].score
            improvement = evaluation.overall_score - last_score
            if improvement < self.min_improvement:
                # 改进停滞，提前终止
                break

        return current_content, self.history