from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional, List

# 定义 API 参数模型
class APIParams(BaseModel):
    action: str = Field(description="要执行的动作")
    entity: str = Field(description="操作的对象")
    filters: List[str] = Field(description="过滤条件", default=[])
    limit: Optional[int] = Field(description="返回数量限制", default=10)

# 创建解析器
parser = PydanticOutputParser(pydantic_object=APIParams)

# Prompt 模板
prompt = ChatPromptTemplate.from_template(
    """将自然语言转换为 API 调用参数。

    自然语言：{query}

    {format_instructions}"""
)

# 组合 Chain
chain = prompt | llm | parser

# 模拟 API 调用函数
def call_api(action: str, entity: str, filters: List[str], limit: int):
    """模拟 API 调用"""
    return {
        "action": action,
        "entity": entity,
        "filters": filters,
        "limit": limit,
        "results": [f"结果{i}" for i in range(min(limit, 3))]
    }

def natural_language_to_api(query: str):
    """自然语言转 API 调用"""
    # 解析参数
    params = chain.invoke({
        "query": query,
        "format_instructions": parser.get_format_instructions()
    })

    # 调用 API
    result = call_api(
        action=params.action,
        entity=params.entity,
        filters=params.filters,
        limit=params.limit or 10
    )

    return result

# 运行示例
result = natural_language_to_api("帮我查找北京的用户，最多返回5个")
print(result)
# {'action': 'search', 'entity': 'user', 'filters': ['北京'], 'limit': 5, 'results': [...]}
