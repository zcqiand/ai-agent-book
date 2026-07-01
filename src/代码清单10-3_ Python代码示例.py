from langchain_core.runnables import RunnableParallel

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 并行处理同一输入
parallel = RunnableParallel(
    summary=llm,
    translation=llm,
    sentiment=llm,
)

# 输入会同时传给三个 LLM
result = parallel.invoke("人工智能正在改变我们的生活方式")
# result = {"summary": "...", "translation": "...", "sentiment": "..."}
