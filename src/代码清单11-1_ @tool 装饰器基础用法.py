from langchain_core.tools import tool

@tool
def search_knowledge_base(query: str) -> str:
    """从知识库搜索相关信息

    Args:
        query: 搜索关键词

    Returns:
        搜索结果摘要
    """
    # 实际实现会调用搜索API
    results = [
        "关于AI大模型的技术文档...",
        "最新研究进展报告...",
    ]
    return "\n".join([r for r in results if query in r])

# 查看自动生成的工具定义
print(search_knowledge_base.name)  # search_knowledge_base
print(search_knowledge_base.description)
# "从知识库搜索相关信息\n\nArgs:\n    query: 搜索关键词\n\nReturns:\n    搜索结果摘要"