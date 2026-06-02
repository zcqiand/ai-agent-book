from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 使用 OpenAI 的 Embedding 模型
embeddings = OpenAIEmbeddings()

# 创建向量存储
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./vector_db"  # 持久化存储
)

print("向量数据库创建成功")