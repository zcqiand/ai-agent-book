from langchain.memory import VectorStoreRetrieverMemory
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 创建向量存储
vectorstore = Chroma.from_texts(
    texts=["用户喜欢中餐", "用户工作繁忙"],
    embedding=OpenAIEmbeddings(),
    persist_directory="./memory_db"
)

memory = VectorStoreRetrieverMemory(
    vectorstore=vectorstore,
    memory_key="retrieved",
    search_kwargs={"k": 2}  # 返回最相关的2条
)

# 保存记忆
memory.save_context(
    {"input": "我喜欢中餐，尤其是川菜"},
    {"output": "好的，已经记住您喜欢川菜"}
)

# 检索记忆
retrieved = memory.load_memory_variables({"query": "用户的饮食偏好"})
print(retrieved["retrieved"])  # 可能返回"用户喜欢中餐"
