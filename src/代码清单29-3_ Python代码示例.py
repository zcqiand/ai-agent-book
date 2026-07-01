from langchain.retrievers import BM25Retriever, VectorStoreRetriever

class RetrieverFactory:
    """检索器工厂"""

    @staticmethod
    def create_bm25_retriever(documents: list) -> BM25Retriever:
        """关键词检索"""
        return BM25Retriever.from_documents(documents)

    @staticmethod
    def create_vector_retriever(
        vectorstore,
        search_type="similarity",
        k=5
    ) -> VectorStoreRetriever:
        """向量检索"""
        return vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs={"k": k}
        )

    @staticmethod
    def create_ensemble_retriever(
        retrievers: list,
        weights: list = None
    ):
        """混合检索"""
        from langchain.retrievers import EnsembleRetriever

        if weights is None:
            weights = [1/len(retrievers)] * len(retrievers)

        return EnsembleRetriever(
            retrievers=retrievers,
            weights=weights
        )
