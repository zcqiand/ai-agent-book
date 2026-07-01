from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)

@tool
def search_web(query: str) -> str:
    """搜索网络信息"""
    return f"网络搜索结果: {query}..."

@tool
def analyze_content(content: str) -> str:
    """分析内容并提取关键信息"""
    return f"分析结果: 在内容中发现了关键信息..."

@tool
def format_output(data: str) -> str:
    """将数据格式化为报告"""
    return f"报告格式: {data}"

# 组合工具
def research_pipeline(query: str):
    """研究管道：搜索 -> 分析 -> 格式化"""
    raw = search_web.invoke(query)
    analyzed = analyze_content.invoke(raw)
    formatted = format_output.invoke(analyzed)
    return formatted

# 运行
result = research_pipeline("AI大模型最新进展")
