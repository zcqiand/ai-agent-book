"""整合：部署底座（FastAPI + LangGraph）+ 可观测（日志+指标）+ 安全
（API Key + RBAC）三层叠成一个能跑的最小生产服务。

一个 POST /chat 端点：
  - 挂 verify_api_key + require_permission(EXECUTE) 两层 Depends；
  - 中间件层挂结构化日志 + Prometheus 指标；
  - 端点内构造 initial state、调 graph.invoke、返回 ChatResponse。

最小整合示意，演示三层叠加的姿态，不展开完整生产配置（PostgresSaver
多副本、OpenTelemetry 完整链路、OAuth2/JWT 身份验证等超出本章范围）。

为节省篇幅，前三清单已定义的代码这里用注释占位、不重复贴出——把本文件
与清单21-1/21-2/21-3 的对应片段拼到一起即可独立运行。
"""
from __future__ import annotations
import logging, time, uuid
from typing import Any

from fastapi import Depends, FastAPI, Request
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from pydantic import BaseModel


# === 第一层：部署底座 —— 复用清单21-1 的图与 Pydantic 契约 =========
# from deploy_app import build_echo_graph, ChatState   # 清单21-1
# class ChatRequest(BaseModel): message: str           # 清单21-1
# class ChatResponse(BaseModel): reply: str            # 清单21-1

_compiled_graph = build_echo_graph()   # 清单21-1 已定义


# === 第二层：可观测 —— 复用清单21-2 的 JsonFormatter / setup_logger /
# Counter / Histogram / observe_request 中间件 =====================
# from observability_app import (
#     JsonFormatter, setup_logger, REQUEST_COUNT, REQUEST_LATENCY,
# )
# logger = setup_logger()                              # 清单21-2
logger = setup_logger()   # 清单21-2 已定义


# === 第三层：安全 —— 复用清单21-3 的 Role / Permission / verify_api_key /
# require_permission ===============================================
# from secure_app import (
#     Role, Permission, verify_api_key, require_permission,
# )                                                    # 清单21-3


# === 整合：FastAPI app + 中间件 + 端点 =============================

app = FastAPI(title="Ch21 Minimal Production Service")


@app.middleware("http")
async def observe(request: Request, call_next):
    """中间件：注入 trace_id、记日志、采指标。三层叠加的「可观测」层。

    与清单21-2 的 observe_request 同款，这里贴出是为让整合文件自包含、
    读者能一眼看到「中间件挂在 app 上」这一步。
    """
    trace_id = uuid.uuid4().hex[:16]
    request.state.trace_id = trace_id
    start = time.perf_counter()
    logger.info("request in", extra={"trace_id": trace_id, "node_name": "middleware"})
    try:
        response = await call_next(request)
        status = response.status_code
    except Exception:
        status = 500
        logger.error("request error",
                     extra={"trace_id": trace_id, "node_name": "middleware"}, exc_info=True)
        raise
    finally:
        latency = time.perf_counter() - start
        REQUEST_LATENCY.labels(method=request.method, path=request.url.path).observe(latency)
        REQUEST_COUNT.labels(method=request.method, path=request.url.path,
                              status=str(status)).inc()
        logger.info("request out", extra={"trace_id": trace_id, "node_name": "middleware"})
    return response


@app.get("/metrics")
def metrics():
    """Prometheus 抓取端点。"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/chat", response_model=ChatResponse)
def chat(
    req: ChatRequest,
    request: Request,
    user_id: str = Depends(require_permission(Permission.EXECUTE)),
):
    """整合端点：三层叠加的核心。

    Depends 链：verify_api_key（认证）→ require_permission(EXECUTE)（授权）。
    中间件已确保 request.state.trace_id 存在，端点取来记业务日志。
    最后调 graph.invoke 跑图——部署底座、可观测、安全三层在此交汇。
    """
    trace_id = getattr(request.state, "trace_id", "-")
    logger.info("chat invoked", extra={"trace_id": trace_id, "node_name": "endpoint.chat"})
    initial: ChatState = {"message": req.message, "reply": ""}
    out = _compiled_graph.invoke(initial)
    logger.info("chat done", extra={"trace_id": trace_id, "node_name": "endpoint.chat"})
    return ChatResponse(reply=out.get("reply", ""))


if __name__ == "__main__":
    import uvicorn
    # host/port 写死只为演示；生产用 uvicorn CLI 或 gunicorn+uvicorn worker
    uvicorn.run(app, host="0.0.0.0", port=8000)