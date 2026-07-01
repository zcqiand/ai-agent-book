from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)

memory = ConversationSummaryMemory(
    llm=llm,  # LLM 用于生成摘要
    memory_key="summary",
    return_messages=True
)

# 使用方式与 BufferMemory 类似
def chat_with_summary(user_input):
    history = memory.load_memory_variables({})

    prompt = f"用户说过：{history['summary']}\n\n最新：{user_input}"
    response = llm.invoke(prompt)

    memory.save_context({"input": user_input}, {"output": response.content})

    return response.content
