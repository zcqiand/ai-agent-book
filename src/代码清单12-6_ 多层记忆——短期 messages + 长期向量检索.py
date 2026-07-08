from langchain.agents import create_agent
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.tools import tool

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 长期记忆：外挂向量存储
long_term_store = Chroma(embedding_function=OpenAIEmbeddings(), persist_directory="./lt_mem")

@tool
def recall_long_term(query: str) -> str:
    """从长期记忆中检索与 query 相关的历史信息。"""
    docs = long_term_store.similarity_search(query, k=2)
    return "\n".join(d.page_content for d in docs) if docs else "（无相关长期记忆）"

# 短期记忆由 create_agent 的 messages 状态自动承载
agent = create_agent(
    model=llm,
    tools=[recall_long_term],
    system_prompt=(
        "你是一个具备多层记忆的助手。当前对话的短期记忆由 messages 自动维护；"
        "若需回忆更早的偏好或事实，调用 recall_long_term 工具检索长期记忆。"
    ),
)

# 使用多层记忆
messages = []
def chat(user_input: str) -> str:
    messages.append({"role": "user", "content": user_input})
    result = agent.invoke({"messages": messages})
    reply = result["messages"][-1].content
    messages.append({"role": "assistant", "content": reply})
    # 把高价值信息写入长期记忆（实际应由 LLM 判断什么值得记）
    long_term_store.add_texts([f"用户说过：{user_input}"])
    return reply

print(chat("我喜欢川菜"))
print(chat("我工作很忙"))
print(chat("根据我的饮食偏好推荐"))  # Agent 会调用 recall_long_term 找回"川菜"