from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

prompt = ChatPromptTemplate.from_template("回答关于{topic}的问题：{question}")

# 先并行分析，再串行生成
analysis_prompt = ChatPromptTemplate.from_template("分析这个问题：{question}")
answer_prompt = ChatPromptTemplate.from_template("基于分析生成回答：{analysis}")

analysis_chain = analysis_prompt | llm
answer_chain = answer_prompt | llm

full_chain = (
    {
        "question": RunnablePassthrough(),
        "analysis": analysis_chain
    }
    | answer_chain
)

result = full_chain.invoke("什么是机器学习？")