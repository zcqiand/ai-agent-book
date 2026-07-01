from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 创建向量存储
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)

# 关键词检索
bm25_retriever = RetrieverFactory.create_bm25_retriever(chunks)

# 向量检索
vector_retriever = RetrieverFactory.create_vector_retriever(vectorstore)

# 混合检索
hybrid_retriever = RetrieverFactory.create_ensemble_retriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.3, 0.7]  # 关键词30%，向量70%
)

# 使用混合检索
results = hybrid_retriever.invoke("如何设置用户权限")
for doc in results:
    print(f"文档: {doc.page_content[:100]}...")
