from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

# 1. 初始化向量数据库
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=OpenAIEmbeddings()
)

# 2. 创建 RAG 检索工具
llm = ChatOpenAI(model="gpt-4", temperature=0)
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)

def rag_search(query):
    """从文档库检索相关信息"""
    return rag_chain.run(query)

# 3. 创建记忆管理工具
from langchain.memory import ConversationSummaryMemory

memory = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history",
    return_messages=True
)

# 4. 组合成 Agent
tools = [
    Tool(name="文档检索", func=rag_search, description="从文档库检索相关信息"),
    # 可以继续添加更多工具
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# 5. 运行
result = agent.run("用户之前问过什么？")
print(result)
