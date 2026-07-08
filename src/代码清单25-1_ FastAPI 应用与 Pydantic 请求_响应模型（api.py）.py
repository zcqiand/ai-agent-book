# 摘自 code/sql-self-healer/src/sql_self_healer/api.py
from fastapi import Depends, FastAPI
from pydantic import BaseModel

from .graph import build_graph
from .llm import make_llm

app = FastAPI(title="SQL Self-Healer")


class QueryRequest(BaseModel):
    """``/query`` 请求体。"""

    query: str
    tenant_id: str = "default"
    db_url: str = "sqlite:///./data/sample.db"


class QueryResponse(BaseModel):
    """``/query`` 响应体。"""

    sql: str
    result: str
    error: str