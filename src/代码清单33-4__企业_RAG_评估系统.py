from typing import List, Dict
from datetime import datetime
import json

class EnterpriseRAGEvaluator:
    """企业级 RAG 评估系统"""

    def __init__(self, rag_system):
        self.rag = rag_system
        self.evaluator = RAGEvaluator(rag_system)
        self.hallucination_detector = HallucinationDetector()
        self.eval_results = []

    def run_evaluation(self, eval_set: List[Dict]) -> Dict:
        """运行完整评估"""
        # 1. 检索评估
        queries = [case["question"] for case in eval_set]
        retrieval_results = self.evaluator.evaluate_retrieval(queries)

        # 2. 生成评估
        generation_results = self.evaluator.evaluate_generation(eval_set)

        # 3. 幻觉检测
        hallucination_results = []
        for case in eval_set:
            response = self.rag.query(case["question"])
            context = case.get("context", "")
            hall_result = self.hallucination_detector.detect(response, context)
            hallucination_results.append(hall_result)

        # 4. 汇总报告
        report = {
            "evaluation_date": datetime.now().isoformat(),
            "total_cases": len(eval_set),
            "retrieval": {
                "avg_recall": retrieval_results["avg_recall"]
            },
            "generation": {
                "avg_faithfulness": generation_results["avg_faithfulness"],
                "avg_relevance": generation_results["avg_relevance"]
            },
            "hallucination": {
                "rate": sum(1 for r in hallucination_results if r["has_hallucination"]) / len(hallucination_results)
            },
            "overall_score": self._calculate_overall_score(
                retrieval_results["avg_recall"],
                generation_results["avg_faithfulness"],
                generation_results["avg_relevance"]
            )
        }

        self.eval_results.append(report)
        return report

    def _calculate_overall_score(
        self,
        recall: float,
        faithfulness: float,
        relevance: float
    ) -> float:
        """计算综合评分"""
        return 0.3 * recall + 0.4 * faithfulness + 0.3 * relevance

    def generate_report(self) -> str:
        """生成评估报告"""
        if not self.eval_results:
            return "暂无评估数据"

        latest = self.eval_results[-1]

        report = f"""
# RAG 系统评估报告

## 评估概况
- 评估日期: {latest['evaluation_date']}
- 测试用例: {latest['total_cases']} 个

## 检索质量
- 平均召回率: {latest['retrieval']['avg_recall']:.2%}

## 生成质量
- 平均忠诚度: {latest['generation']['avg_faithfulness']:.2%}
- 平均相关性: {latest['generation']['avg_relevance']:.2%}

## 幻觉检测
- 幻觉率: {latest['hallucination']['rate']:.2%}

## 综合评分
- 总体得分: {latest['overall_score']:.2%}

## 优化建议
{self._generate_suggestions(latest)}
"""
        return report

    def _generate_suggestions(self, results: Dict) -> str:
        """生成优化建议"""
        suggestions = []

        if results["retrieval"]["avg_recall"] < 0.7:
            suggestions.append("- 检索召回率偏低，建议优化查询改写或增加向量存储")

        if results["generation"]["avg_faithfulness"] < 0.8:
            suggestions.append("- 生成忠诚度偏低，建议检查上下文构建或更换模型")

        if results["hallucination"]["rate"] > 0.1:
            suggestions.append("- 幻觉率偏高，建议增加事实核查环节")

        return "\n".join(suggestions) if suggestions else "- 系统表现良好，继续保持"

# 使用
evaluator = EnterpriseRAGEvaluator(rag_system)

# 运行评估
report = evaluator.run_evaluation(eval_set)
print(f"评估结果: {report}")

# 生成报告
print(evaluator.generate_report())