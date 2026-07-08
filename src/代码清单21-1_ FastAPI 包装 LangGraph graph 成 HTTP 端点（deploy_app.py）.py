"""最小部署示意：用 FastAPI 把一个 LangGraph 图暴露成 HTTP 端点。

图本身只有一个 echo 节点（不调 LLM、不连外部服务），让读者复制即可
跑通「HTTP 请求 → graph.invoke → HTTP 响应」这条链，专注部署姿态本身，
不被 LLM 接入的复杂度干扰。
"""
from __future__ import annotations
from typing import TypedDict

from fastapi import FastAPI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel


# --- 1. 图的定义：最小 echo 图 --------------------------------------

class ChatState(TypedDict, total=False):
    """图的状态：message 进、reply 出。total=False 让字段可选。"""
    message: str
    reply: str


def echo_node(state: ChatState) -> ChatState:
    """echo 节点：把 message 原样回填到 reply。

    真实生产里这里会换成调 LLM、查知识库等节点；本章用 echo 是为了让
    部署姿态可独立验证，不被 LLM 的网络/Key 依赖拖住。
    """
    return {"reply": f"echo: {state.get('message', '')}"}


def build_echo_graph():
    """装配并编译一个最小图：START → echo_node → END。"""
    graph = StateGraph(ChatState)
    graph.add_node("echo", echo_node)
    graph.add_edge(START, "echo")
    graph.add_edge("echo", END)
    # 无 checkpointer：本章只演示部署，持久化是 ch19/ch26 的主题
    return graph.compile()


# --- 2. FastAPI 应用 + Pydantic 契约 --------------------------------

app = FastAPI(title="Ch21 Deploy Demo")
# 图在应用启动时编译一次，进程内复用；避免每个请求重编译的开销
_compiled_graph = build_echo_graph()


class ChatRequest(BaseModel):
    """``/chat`` 请求体。"""
    message: str


class ChatResponse(BaseModel):
    """``/chat`` 响应体。"""
    reply: str


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    """把请求跑过 echo 图，返回 reply。

    端点本身是个翻译器：把 ChatRequest 翻译成图的 initial state，
    再把图吐出的 state 翻译回 ChatResponse。这与卷四 ch25 的 /query
    端点同款形态，只是图更小、不接 LLM。
    """
    initial: ChatState = {"message": req.message, "reply": ""}
    out = _compiled_graph.invoke(initial)
    return ChatResponse(reply=out.get("reply", ""))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)