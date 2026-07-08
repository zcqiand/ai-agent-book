from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 创建向量存储，持久化到本地
vectorstore = Chroma.from_texts(
    texts=["用户喜欢中餐", "用户工作繁忙"],
    embedding=OpenAIEmbeddings(),
    persist_directory="./memory_db"
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})  # 返回最相关的2条

def chat_with_retrieval(user_input: str) -> str:
    # 用当前问题检索相关的历史记忆
    docs = retriever.invoke(user_input)
    recalled = "\n".join(d.page_content for d in docs)

    # 把检索到的记忆注入 system_prompt（再交给 create_agent 推理）
    system_prompt = (
        f"你是一个有记忆的助手。相关历史记忆：\n{recalled}"
    )
    # agent = create_agent(model=llm, tools=[], system_prompt=system_prompt)
    # return agent.invoke({"messages": [...]})["messages"][-1].content
    return f"[召回记忆] {recalled}\n[回复] 关于「{user_input}」..."

# 检索记忆
print(chat_with_retrieval("用户的饮食偏好"))
# 可能返回包含"用户喜欢中餐"的回复