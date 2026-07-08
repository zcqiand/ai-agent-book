from langchain_community.retrievers import EnsembleRetriever

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

# 使用混合检索的 Chain（同样用 LCEL 手搓，把 retriever 换成 ensemble_retriever 即可）
def qa_chain_mixed(question: str) -> dict:
    docs = ensemble_retriever.invoke(question)
    context = "\n".join(d.page_content for d in docs)
    messages = prompt.format_messages(context=context, question=question)
    answer = llm.invoke(messages).content
    return {"answer": answer, "source_documents": docs}