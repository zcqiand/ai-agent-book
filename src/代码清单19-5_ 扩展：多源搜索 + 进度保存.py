from langgraph.graph import StateGraph, END
from typing import TypedDict
import json

class ExtendedResearchState(TypedDict):
    topic: str
    plan: list
    current_source: str  # 当前搜索源
    sources: list        # 可用搜索源
    results: dict        # 各源搜索结果
    report: str

def multi_source_search(state: ExtendedResearchState) -> ExtendedResearchState:
    """多源搜索"""
    sources = state.get("sources", ["web", "docs", "db"])
    results = {}

    for source in sources:
        if source == "web":
            results["web"] = search_web(state["topic"])
        elif source == "docs":
            results["docs"] = search_docs(state["topic"])
        elif source == "db":
            results["db"] = search_database(state["topic"])

    return {
        **state,
        "results": results
    }

def save_progress(state: ExtendedResearchState, filepath: str):
    """保存研究进度"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(dict(state), f, ensure_ascii=False)
    print(f"进度已保存到 {filepath}")

def load_progress(filepath: str) -> ExtendedResearchState:
    """加载研究进度"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def user_feedback(state: ExtendedResearchState, feedback: str) -> ExtendedResearchState:
    """处理用户反馈"""
    # 根据用户反馈调整研究方向
    adjustment = llm.invoke(f"""
    用户反馈：{feedback}

    当前研究方向：{state.get('topic')}

    请给出调整建议：""")

    return {
        **state,
        "topic": adjustment  # 可以修改主题
    }
