from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List

class SearchResult(BaseModel):
    query: str
    results: List[str]
    total: int

parser = PydanticOutputParser(pydantic_object=SearchResult)

def robust_parse(text: str, max_retries: int = 3):
    """带重试的解析"""
    for i in range(max_retries):
        try:
            return parser.parse(text)
        except Exception as e:
            print(f"解析失败，重试 {i+1}/{max_retries}: {e}")
            # 可以在此处添加重试逻辑
    return None

# 使用
result = robust_parse(llm.invoke("返回搜索结果"))