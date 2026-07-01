from langchain_openai import OpenAIEmbeddings
import numpy as np

class Reranker:
    """检索结果重排器"""

    def __init__(self, embeddings: OpenAIEmbeddings):
        self.embeddings = embeddings

    def rerank(self, query: str, documents: list, top_k: int = 5) -> list:
        """对检索结果进行重排"""
        if not documents:
            return []

        # 计算查询与每个文档的语义相似度
        query_embedding = self.embeddings.embed_query(query)
        doc_embeddings = [
            self.embeddings.embed_query(doc.page_content)
            for doc in documents
        ]

        # 计算余弦相似度
        similarities = []
        for doc_emb in doc_embeddings:
            sim = self._cosine_similarity(query_embedding, doc_emb)
            similarities.append(sim)

        # 按相似度排序
        indexed = list(enumerate(similarities))
        indexed.sort(key=lambda x: x[1], reverse=True)

        # 返回重排后的文档
        reranked = [documents[i] for i, _ in indexed[:top_k]]
        return reranked

    def _cosine_similarity(self, a: list, b: list) -> float:
        """余弦相似度"""
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

reranker = Reranker(OpenAIEmbeddings())
results = reranker.rerank("年假政策", documents, top_k=3)
