from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

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

# 3. 创建检索链
llm = ChatOpenAI(model="gpt-4", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)

# 4. 问答
query = "这篇文档的核心观点是什么？"
result = qa_chain.run(query)
print(result)
