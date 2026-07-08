from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 检索器：取最相关的 5 个文档块
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# 提示模板：context 注入检索内容，question 是用户问题
prompt = ChatPromptTemplate.from_template(
    "你是一名严谨的知识库助手。请只依据下面的资料回答问题，"
    "资料中没有的内容请直接说「资料中未提及」。\n\n"
    "【资料】\n{context}\n\n【问题】{question}"
)

def qa_chain_invoke(question: str) -> dict:
    """检索 + 拼 context + 生成，等价于旧版 chain_type='stuff' + return_source_documents=True。"""
    docs = retriever.invoke(question)                       # 检索 Top-K 文档块
    context = "\n".join(d.page_content for d in docs)       # 拼成一段 context
    messages = prompt.format_messages(context=context, question=question)
    answer = llm.invoke(messages).content                  # LLM 基于检索内容生成
    return {"answer": answer, "source_documents": docs}    # 源文档一并返回，便于溯源

# 问答
question = "公司的年假政策是什么？"
result = qa_chain_invoke(question)

print(f"回答: {result['answer']}")
print(f"参考文档数: {len(result['source_documents'])}")