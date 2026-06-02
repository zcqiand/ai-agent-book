from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 创建 Chain
prompt = ChatPromptTemplate.from_template("用{style}风格解释{concept}")
chain = prompt | llm

# 运行 - 自动追踪
result = chain.invoke({"style": "专业", "concept": "大语言模型"})
print(result.content)