from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

# 定义输出格式
class MovieReview(BaseModel):
    title: str = Field(description="电影名称")
    rating: float = Field(description="评分，1-10分")
    summary: str = Field(description="剧情简介")
    pros: List[str] = Field(description="优点列表")
    cons: List[str] = Field(description="缺点列表")

# 创建解析器
parser = PydanticOutputParser(pydantic_object=MovieReview)

# Prompt 模板
prompt = ChatPromptTemplate.from_template(
    """请评论电影《{movie}》。

    {format_instructions}"""
)

# 组合 Chain
chain = prompt | llm | parser

# 运行
result = chain.invoke({
    "movie": "盗梦空间",
    "format_instructions": parser.get_format_instructions()
})

print(result.title)      # 盗梦空间
print(result.rating)     # 9.5
print(result.pros)       # ['剧情紧凑', '视觉效果震撼', ...]