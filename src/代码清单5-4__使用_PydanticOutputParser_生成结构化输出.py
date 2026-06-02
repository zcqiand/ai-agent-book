from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

# 定义输出格式
class AnswerWithReasons(BaseModel):
    answer: str = Field(description="对问题的直接回答")
    reasons: List[str] = Field(description="支持答案的3个理由")
    confidence: float = Field(description="对答案的信心程度，0-1之间")

# 创建解析器
parser = PydanticOutputParser(pydantic_object=AnswerWithReasons)

# 创建提示词（包含解析器的格式说明）
prompt = ChatPromptTemplate.from_template(
    """请回答以下问题，并按指定格式输出。
    
    问题：{question}
    
    {format_instructions}"""
)

# 组合 Chain
chain = prompt | llm | parser

# 调用 Chain
result = chain.invoke({
    "question": "人工智能会取代人类的工作吗？",
    "format_instructions": parser.get_format_instructions()
})

print(f"回答：{result.answer}")
print(f"理由：{result.reasons}")
print(f"信心：{result.confidence}")