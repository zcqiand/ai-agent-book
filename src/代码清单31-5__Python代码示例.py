from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

class RAGOptimizer:
    """RAG 性能优化器"""

    def __init__(self, persist_dir: str = "./chroma_db"):
        self.embeddings = OpenAIEmbeddings()
        self.persist_dir = persist_dir
        self.vectorstore = None
        self.hybrid_retriever = None

    def load_documents(self, docs: list):
        """加载文档"""
        self.vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )

    def evaluate_retrieval(self, query: str, ground_truth: list) -> dict:
        """评估检索性能"""
        # 原始检索
        raw_results = self.vectorstore.similarity_search(query, k=10)

        # 改写后检索
        rewriter = QueryRewriter()
        refined_query = rewriter.rewrite(query)
        refined_results = self.vectorstore.similarity_search(refined_query, k=10)

        # 计算召回率
        raw_recall = self._calculate_recall(raw_results, ground_truth)
        refined_recall = self._calculate_recall(refined_results, ground_truth)

        return {
            "原始召回率": raw_recall,
            "改写后召回率": refined_recall,
            "提升": refined_recall - raw_recall
        }

    def _calculate_recall(self, retrieved: list, relevant: list) -> float:
        """计算召回率"""
        retrieved_ids = set([doc.metadata.get("id") for doc in retrieved])
        relevant_ids = set(relevant)
        return len(retrieved_ids & relevant_ids) / len(relevant_ids) if relevant_ids else 0

# 使用
optimizer = RAGOptimizer()
optimizer.load_documents(documents)

# 评估
eval_result = optimizer.evaluate_retrieval(
    query="年假如何计算",
    ground_truth=["doc1", "doc2", "doc3"]
)
print(f"评估结果: {eval_result}")