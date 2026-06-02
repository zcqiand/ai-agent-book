from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

vectorstore = Chroma(persist_directory="./vector_db", embedding=OpenAIEmbeddings())
llm = ChatOpenAI(model="gpt-4", temperature=0)

rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5})
)

def rag_search(query):
    """从知识库检索"""
    return rag_chain.run(query)