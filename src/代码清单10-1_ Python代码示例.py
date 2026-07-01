from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 简单管道
prompt = ChatPromptTemplate.from_template("解释{concept}")
chain = prompt | llm

result = chain.invoke({"concept": "大语言模型"})
print(result.content)
