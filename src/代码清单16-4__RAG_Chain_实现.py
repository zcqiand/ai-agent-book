from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 创建检索链
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # 将所有检索内容塞进一个prompt
    retriever=vectorstore.as_retriever(
        search_kwargs={"k": 5}  # 返回最相关的5个块
    ),
    return_source_documents=True  # 返回源文档用于溯源
)

# 问答
question = "公司的年假政策是什么？"
result = qa_chain({"query": question})

print(f"回答: {result['result']}")
print(f"参考文档数: {len(result['source_documents'])}")