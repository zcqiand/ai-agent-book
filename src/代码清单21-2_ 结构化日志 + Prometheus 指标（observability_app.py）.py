"""可观测性三件套之：结构化日志 + Prometheus 指标。

一个 FastAPI 中间件在请求进出时：
  1) 用 JSON 格式记录日志（含 trace_id、node_name，便于聚合检索）；
  2) 更新 prometheus_client 的 Counter（请求数）与 Histogram（延迟）。
OpenTelemetry 的完整集成不在本章展开——生产可用 OpenTelemetry SDK 把
trace_id 真正贯穿 HTTP → graph.invoke → 节点；这里在日志层演示 trace_id
如何生成与携带，链路追踪的实现细节留给读者按官方文档接入。
"""
from __future__ import annotations
import json, logging, time, uuid
from typing import Any

from fastapi import FastAPI, Request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest


# --- 1. 结构化日志：JSON formatter ----------------------------------

class JsonFormatter(logging.Formatter):
    """把 LogRecord 格式化成单行 JSON。

    为什么用 JSON 而非纯文本：生产环境的日志会被 ELK / Loki 这类系统
    采集，JSON 字段可被直接索引检索（按 trace_id、level 过滤），纯文本
    得写正则解析、易错且慢。
    """
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "trace_id": getattr(record, "trace_id", "-"),
            "node_name": getattr(record, "node_name", "-"),
            "message": record.getMessage(),
        }
        return json.dumps(payload, ensure_ascii=False)


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("ch21.obs")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter(datefmt="%Y-%m-%dT%H:%M:%S"))
        logger.addHandler(handler)
    return logger


logger = setup_logger()


# --- 2. Prometheus 指标 ---------------------------------------------

# 标签 method/path/status 能按「哪个端点、什么状态码」分别聚合
REQUEST_COUNT = Counter(
    "http_requests_total", "HTTP 请求总数", ["method", "path", "status"]
)
REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds", "HTTP 请求延迟（秒）", ["method", "path"]
)


# --- 3. FastAPI 应用 + 中间件 + /metrics 端点 -----------------------

app = FastAPI(title="Ch21 Observability Demo")


@app.middleware("http")
async def observe_request(request: Request, call_next):
    """每个 HTTP 请求进出时记日志 + 更新指标 + 注入 trace_id。

    trace_id 在这里用 uuid4 现场生成并塞进 request.state，端点和日志
    都能读到它——这是「链路追踪」的最朴素形态：一次请求一个唯一 id，
    所有相关日志共享这个 id，按它一过滤就能还原整条链路。
    """
    trace_id = uuid.uuid4().hex[:16]
    request.state.trace_id = trace_id
    start = time.perf_counter()
    logger.info("request in", extra={"trace_id": trace_id, "node_name": "middleware.request"})
    try:
        response = await call_next(request)
        status = response.status_code
    except Exception:
        status = 500
        logger.error("request error",
                     extra={"trace_id": trace_id, "node_name": "middleware.request"},
                     exc_info=True)
        raise
    finally:
        latency = time.perf_counter() - start
        REQUEST_LATENCY.labels(method=request.method, path=request.url.path).observe(latency)
        REQUEST_COUNT.labels(method=request.method, path=request.url.path,
                              status=str(status)).inc()
        logger.info("request out", extra={"trace_id": trace_id, "node_name": "middleware.request"})
    return response


@app.get("/metrics")
def metrics():
    """Prometheus 抓取端点。"""
    from fastapi.responses import Response
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/ping")
def ping(request: Request):
    """演示端点：能从 request.state 读到中间件注入的 trace_id。"""
    trace_id = getattr(request.state, "trace_id", "-")
    logger.info("ping handled", extra={"trace_id": trace_id, "node_name": "endpoint.ping"})
    return {"ok": True, "trace_id": trace_id}