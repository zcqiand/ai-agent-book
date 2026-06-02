from langchain.agents import AgentType, initialize_agent, Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(model="gpt-4", temperature=0)

# 工具定义
def web_search(query: str) -> str:
    """模拟网络搜索"""
    return f"网络搜索结果: 关于{query}的最新信息..."

def read_document(doc_id: str) -> str:
    """模拟读取文档"""
    return f"文档{doc_id}的内容..."

tools = [
    Tool(name="网络搜索", func=web_search, description="搜索网络信息"),
    Tool(name="读取文档", func=read_document, description="读取指定ID的文档"),
]

# 创建 Agent
research_agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True
)

# 运行研究任务
result = research_agent.run(
    """请研究以下主题：AI大模型在医疗领域的应用
    1. 先进行网络搜索了解概况
    2. 查找相关技术文档
    3. 综合信息生成报告
    """
)

print(result)

# 增强版：使用 LangGraph 实现更精细的控制
from langgraph.graph import StateGraph, END
from typing import TypedDict

class ResearchState(TypedDict):
    topic: str
    findings: list
    report: str

def search_phase(state):
    """搜索阶段"""
    result = web_search(state["topic"])
    return {"findings": [result]}

def research_phase(state):
    """研究阶段"""
    docs = [read_document(f"doc_{i}") for i in range(3)]
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