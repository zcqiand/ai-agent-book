from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# 1. 初始化向量数据库
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=OpenAIEmbeddings()
)

# 2. 用 LCEL 手搓 RAG 检索链（RetrievalQA 在 1.x 已移除）
#    retriever.invoke 取文档 → 拼 context → llm.invoke 生成
llm = ChatOpenAI(model="gpt-4", temperature=0)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
rag_prompt = ChatPromptTemplate.from_template(
    "根据以下资料回答问题：\n{context}\n问题：{question}"
)

def _rag_search(question: str) -> str:
    docs = retriever.invoke(question)
    context = "\n".join(d.page_content for d in docs)
    return llm.invoke(rag_prompt.format_messages(context=context, question=question)).content

# 3. 把检索包装成 Agent 工具：@tool 装饰器自动登记函数名/描述/参数schema
@tool
def doc_search(query: str) -> str:
    """从文档库检索相关信息，用于回答与已有知识库相关的问题。"""
    return _rag_search(query)

tools = [
    doc_search,
    # 可以继续添加更多工具，例如网络搜索、日历查询等
]

# 4. 用 create_agent 组合成 Agent（1.x 推荐，走模型原生 tool-calling）
#    create_agent 返回一个 LangGraph CompiledStateGraph，invoke 时传 messages
#    短期记忆由 Agent 自带的 messages 状态承载（跨多轮对话自动累积上下文）；
#    若需跨会话长期记忆，可在 system_prompt 里注入外部摘要，或外挂 store
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "你是一个能够检索文档库的助手。对涉及已有知识的问题，"
        "调用 doc_search 工具获取最新信息后再作答。"
    ),
    debug=True,  # 等价于旧版的 verbose=True，打印每一步执行轨迹
)

# 5. 运行
result = agent.invoke({
    "messages": [{"role": "user", "content": "用户之前问过什么？"}]
})
print(result["messages"][-1].content)