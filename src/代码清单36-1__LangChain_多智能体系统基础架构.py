from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

# 初始化LLM
llm = ChatOpenAI(model="gpt-4")

# 定义订单Agent
order_agent_system = """你是一名订单查询专家。
你的职责是根据用户提供的订单号，查询订单状态和详情。
只返回订单信息，不要做物流分析或财务建议。"""

def order_query_node(state: dict) -> dict:
    """订单查询节点"""
    messages = [
        SystemMessage(content=order_agent_system),
        HumanMessage(content=state.get("user_query", ""))
    ]
    response = llm.invoke(messages)
    return {
        "order_info": response.content,
        "messages": state.get("messages", []) + [response]
    }

# 定义物流Agent
logistics_agent_system = """你是一名物流分析专家。
根据订单信息，分析最优物流方案。
考虑送达时间、运费、库存情况等因素。"""

def logistics_analysis_node(state: dict) -> dict:
    """物流分析节点"""
    order_info = state.get("order_info", "")
    messages = [
        SystemMessage(content=logistics_agent_system),
        HumanMessage(content=f"订单信息：{order_info}")
    ]
    response = llm.invoke(messages)
    return {
        "logistics_plan": response.content,
        "messages": state.get("messages", []) + [response]
    }

print("多智能体节点定义完成")