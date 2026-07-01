from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import JsonOutputParser

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 创建解析器
parser = JsonOutputParser()

# 创建带格式说明的 Prompt
prompt = ChatPromptTemplate.from_template(
    """回答用户问题，输出 JSON 格式。

    问题：{question}

    {format_instructions}"""
)

# 组合 Chain
chain = prompt | llm | parser

# 运行
result = chain.invoke({
    "question": "人工智能是什么？",
    "format_instructions": parser.get_format_instructions()
})

print(result)  # {'answer': '人工智能是...', 'confidence': 0.9}
