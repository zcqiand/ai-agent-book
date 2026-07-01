from langchain_core.runnables import RunnablePassthrough

# 不使用 Passthrough，输入的 question 会丢失
chain_without = (
    {"analysis": analysis_chain}
    | answer_prompt
    | llm
)

# 使用 Passthrough，保留 question 字段
chain_with = (
    {
        "question": RunnablePassthrough(),
        "analysis": analysis_chain
    }
    | answer_prompt
    | llm
)
