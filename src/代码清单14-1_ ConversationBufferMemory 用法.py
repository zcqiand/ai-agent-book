from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 创建记忆
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 在对话中使用
def chat_with_memory(user_input):
    # 获取历史
    history = memory.load_memory_variables({})

    # 生成回复
    prompt = f"历史对话：{history['chat_history']}\n\n用户：{user_input}"
    response = llm.invoke(prompt)

    # 保存对话
    memory.save_context({"input": user_input}, {"output": response.content})

    return response.content

# 多轮对话示例
chat_with_memory("我叫张三")
chat_with_memory("记住我叫什么了吗？")  # 能回答"张三"
