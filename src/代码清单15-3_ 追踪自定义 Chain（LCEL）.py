from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate  # 1.x：从 langchain_core 导入

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 创建 Chain（LCEL 写法：prompt | llm 用管道符串联）
prompt = ChatPromptTemplate.from_template("用{style}风格解释{concept}")
chain = prompt | llm

# 运行 —— LCEL Chain 同样会被 LangSmith 自动追踪
result = chain.invoke({"style": "专业", "concept": "大语言模型"})
print(result.content)