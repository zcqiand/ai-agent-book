from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from typing import List, Dict, Tuple
import json

class RAGEvaluator:
    """RAG 系统评估器"""

    def __init__(self, rag_system, ground_truth: List[Dict] = None):
        self.rag = rag_system
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.embeddings = OpenAIEmbeddings()
        self.ground_truth = ground_truth or []

    def evaluate_retrieval(self, queries: List[str]) -> Dict:
        """评估检索质量"""
        results = []

        for query in queries:
            # 获取检索结果
            docs = self.rag.vectorstore.similarity_search(query, k=10)

            # 计算召回率
            relevant_ids = self._get_relevant_docs(query)
            retrieved_ids = [doc.metadata.get("id") for doc in docs]

            recall = len(set(relevant_ids) & set(retrieved_ids)) / len(relevant_ids) if relevant_ids else 0

            results.append({
                "query": query,
                "recall": recall,
                "retrieved_count": len(retrieved_ids),
                "relevant_count": len(relevant_ids)
            })

        # 汇总
        avg_recall = sum(r["recall"] for r in results) / len(results)
        return {
            "avg_recall": avg_recall,
            "per_query": results
        }

    def evaluate_generation(self, test_cases: List[Dict]) -> Dict:
        """评估生成质量"""
        results = []

        for case in test_cases:
            question = case["question"]
            expected = case.get("expected_answer", "")

            # 获取回答
            response = self.rag.query(question)

            # 评估各项指标
            faithfulness = self._check_faithfulness(response, case.get("context", ""))
            relevance = self._check_relevance(question, response)
            accuracy = self._check_accuracy(response, expected) if expected else None

            results.append({
                "question": question,
                "answer": response,
                "faithfulness": faithfulness,
                "relevance": relevance,
                "accuracy": accuracy
            })

        avg_faithfulness = sum(r["faithfulness"] for r in results) / len(results)
        avg_relevance = sum(r["relevance"] for r in results) / len(results)

        return {
            "avg_faithfulness": avg_faithfulness,
            "avg_relevance": avg_relevance,
            "per_case": results
        }

    def _get_relevant_docs(self, query: str) -> List[str]:
        """获取查询的相关文档 ID"""
        # 简化实现：实际应使用标注数据
        return []

    def _check_faithfulness(self, answer: str, context: str) -> float:
        """检查回答对上下文的忠诚度"""
        prompt = f"""评估以下回答是否忠实于给定上下文。
        只根据上下文中的信息回答，如果回答中的信息在上下文中找不到，标记为不忠实。

        上下文: {context}
        回答: {answer}

        评估结果（0-1之间的分数，1表示完全忠实）:"""

        response = self.llm.invoke(prompt)
        try:
            score = float(response.content.strip())
            return max(0, min(1, score))
        except:
            return 0.5

    def _check_relevance(self, question: str, answer: str) -> float:
        """检查回答与问题的相关性"""
        prompt = f"""评估以下回答与问题的相关性。

        问题: {question}
        回答: {answer}

        评估结果（0-1之间的分数，1表示完全相关）:"""

        response = self.llm.invoke(prompt)
        try:
            score = float(response.content.strip())
            return max(0, min(1, score))
        except:
            return 0.5

    def _check_accuracy(self, answer: str, expected: str) -> float:
        """检查回答准确性"""
        prompt = f"""评估以下两个回答的含义一致性。

        回答1: {answer}
        回答2: {expected}

        评估结果（0-1之间的分数，1表示完全一致）:"""

        response = self.llm.invoke(prompt)
        try:
            score = float(response.content.strip())
            return max(0, min(1, score))
        except:
            return 0.5
