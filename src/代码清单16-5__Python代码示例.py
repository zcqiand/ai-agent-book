from langchain.retrievers import EnsembleRetriever

# 关键词检索
keyword_retriever = vectorstore.as_retriever(
    search_type="mmr",  # 最大边际相关性
    search_kwargs={"k": 5, "fetch_k": 20}
)

# 向量检索
vector_retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)

# 混合检索
ensemble_retriever = EnsembleRetriever(
    retrievers=[keyword_retriever, vector_retriever],
    weights=[0.3, 0.7]  # 关键词权重0.3，向量权重0.7
)

# 使用混合检索的 Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=ensemble_retriever
)