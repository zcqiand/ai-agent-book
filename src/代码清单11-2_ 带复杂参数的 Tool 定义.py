from langchain_core.tools import tool
from pydantic import BaseModel, Field

class SearchParams(BaseModel):
    query: str = Field(description="搜索关键词")
    source: str = Field(description="信息来源", default="general")
    limit: int = Field(description="返回结果数量", default=5)

@tool
def advanced_search(params: SearchParams) -> str:
    """执行高级搜索

    支持指定信息源和返回数量
    """
    return f"从{params.source}搜索到{params.limit}条结果：..."

# 使用工具
result = advanced_search.invoke({"query": "AI", "source": "tech", "limit": 3})