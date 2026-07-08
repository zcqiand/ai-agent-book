prompt1 = ChatPromptTemplate.from_template("将以下文本翻译成英文：{text}")
prompt2 = ChatPromptTemplate.from_template("将以下英文文本缩写为一句话：{text}")

chain = prompt1 | llm | prompt2 | llm

result = chain.invoke({"text": "人工智能是计算机科学的一个分支，致力于开发能够模拟人类智能的系统"})
print(result.content)