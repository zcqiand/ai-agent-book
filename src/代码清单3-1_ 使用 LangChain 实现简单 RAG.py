from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

# 1. 文档加载与分块
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# 假设 documents 是加载好的文档列表
# texts = text_splitter.split_documents(documents)

# 2. 创建向量存储
vectorstore = Chroma.from_texts(
    texts=[t.page_content for t in texts],
    embedding=OpenAIEmbeddings(),
    persist_directory="./chroma_db"
)

# 3. 用 LCEL 手搓「检索→拼 context→生成」一条链
#    LangChain 1.x 已移除 RetrievalQA（旧版 chains 子模块整体废弃），
#    改用 retriever.invoke 取文档 + ChatPromptTemplate + llm.invoke 显式拼装
llm = ChatOpenAI(model="gpt-4", temperature=0)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

prompt = ChatPromptTemplate.from_template(
    "根据以下资料回答问题：\n{context}\n问题：{question}"
)

def qa_chain_invoke(question: str) -> str:
    docs = retriever.invoke(question)  # 取 Top-K 文档块
    context = "\n".join(d.page_content for d in docs)  # 等价于旧版 chain_type="stuff"
    messages = prompt.format_messages(context=context, question=question)
    return llm.invoke(messages).content

# 4. 问答
query = "这篇文档的核心观点是什么？"
result = qa_chain_invoke(query)
print(result)