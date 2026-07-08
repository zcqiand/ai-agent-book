from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 用 @tool 装饰器登记工具，docstring 自动成为工具描述
@tool
def web_search(query: str) -> str:
    """搜索网络信息。"""
    return f"网络搜索结果: 关于{query}的最新信息..."

@tool
def read_document(doc_id: str) -> str:
    """读取指定ID的文档。"""
    return f"文档{doc_id}的内容..."

tools = [web_search, read_document]

# 用 create_agent 组合成 Agent（1.x 推荐，走模型原生 tool-calling）
research_agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "你是一个研究助手。先规划搜索步骤，多轮调用工具收集信息，"
        "最后综合生成研究报告。"
    ),
    debug=True,
)

# 运行研究任务：invoke 传 messages，取最后一条消息的 content
result = research_agent.invoke({
    "messages": [{"role": "user", "content": (
        "请研究以下主题：AI大模型在医疗领域的应用\n"
        "1. 先进行网络搜索了解概况\n"
        "2. 查找相关技术文档\n"
        "3. 综合信息生成报告"
    )}]
})

print(result["messages"][-1].content)

# 增强版：使用 LangGraph 实现更精细的控制
from langgraph.graph import StateGraph, END
from typing import TypedDict

class ResearchState(TypedDict):
    topic: str
    findings: list
    report: str

def search_phase(state):
    """搜索阶段"""
    result = web_search.invoke({"query": state["topic"]})
    return {"findings": [result]}

def research_phase(state):
    """研究阶段"""
    docs = [read_document.invoke({"doc_id": f"doc_{i}"}) for i in range(3)]
    return {"findings": state.get("findings", []) + docs}

def report_phase(state):
    """报告阶段"""
    findings = state.get("findings", [])
    prompt = f"基于以下发现生成报告：{findings}"
    report = llm.invoke(prompt)
    return {"report": report}

workflow = StateGraph(ResearchState)
workflow.add_node("search", search_phase)
workflow.add_node("research", research_phase)
workflow.add_node("report", report_phase)
workflow.set_entry_point("search")
workflow.add_edge("search", "research")
workflow.add_edge("research", "report")
workflow.add_edge("report", END)

app = workflow.compile()
final_result = app.invoke({
    "topic": "AI大模型在医疗领域的应用",
    "findings": [],
    "report": ""
})

print(final_result["report"])