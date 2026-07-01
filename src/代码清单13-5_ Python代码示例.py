from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from typing import Literal

llm = ChatOpenAI(model="gpt-4", temperature=0)

@tool
def web_search(query: str) -> str:
    """搜索网络信息"""
    return f"搜索结果 for {query}: ..."

@tool
def summarize(text: str, max_length: int = 100) -> str:
    """将长文本摘要为指定长度"""
    # 简化实现
    return text[:max_length] + "..."

@tool
def translate(text: str, target_lang: str = "中文") -> str:
    """翻译文本到目标语言"""
    return f"[翻译为{target_lang}]: {text}"

@tool
def dispatch_task(task: str, params: dict) -> str:
    """智能调度任务到合适的工具

    Args:
        task: 任务类型 (search/summarize/translate)
        params: 任务参数
    """
    if task == "search":
        return web_search.invoke(params.get("query", ""))
    elif task == "summarize":
        return summarize.invoke(params.get("text", ""), params.get("max_length", 100))
    elif task == "translate":
        return translate.invoke(params.get("text", ""), params.get("target_lang", "中文"))
    return "未知任务类型"

# 使用调度器
result = dispatch_task.invoke({
    "task": "search",
    "params": {"query": "AI最新进展"}
})

print(result)
