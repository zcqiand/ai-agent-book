from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.retrievers import BM25Retriever
from langchain.retrievers.ensemble import EnsembleRetriever

class HybridRetriever:
    """混合检索器"""

    def __init__(self, documents: list, embeddings: OpenAIEmbeddings):
        self.documents = documents
        self.embeddings = embeddings

        # 创建向量存储
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=embeddings
        )

        # 创建 BM25 检索器
        self.bm25_retriever = BM25Retriever.from_documents(documents)

        # 创建向量检索器
        self.vector_retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 10}
        )

    def get_ensemble_retriever(self, weights: list = None):
        """获取混合检索器"""
        if weights is None:
            weights = [0.3, 0.7]  # BM25 30%, 向量 70%

        return EnsembleRetriever(
            retrievers=[self.bm25_retriever, self.vector_retriever],
            weights=weights
        )

    def search(self, query: str, k: int = 5):
        """搜索"""
        ensemble = self.get_ensemble_retriever()
        return ensemble.invoke(query)[:k]