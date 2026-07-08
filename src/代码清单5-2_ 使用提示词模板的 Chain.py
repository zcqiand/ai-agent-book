from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 创建提示词模板
prompt = ChatPromptTemplate.from_template(
    "请用{style}风格，解释{concept}，要求不超过{word_count}字。"
)

# 使用管道操作符组合
chain = prompt | llm

# 调用 Chain
response = chain.invoke({
    "style": "专业学术",
    "concept": "大语言模型",
    "word_count": 100
})
print(response.content)