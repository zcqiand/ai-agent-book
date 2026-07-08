# 摘自 code/sql-self-healer/src/sql_self_healer/api.py
@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest, llm=Depends(get_llm)) -> QueryResponse:
    """把自然语言查询跑过自愈状态机，返回最终 SQL / 结果 / 报错。"""
    graph = build_graph(llm=llm, db_url=req.db_url)
    initial = {
        "query": req.query,
        "sql": "",
        "error": "",
        "retries": 0,
        "result": "",
        "tenant_id": req.tenant_id,
        "approved": True,
    }
    out = graph.invoke(initial)
    return QueryResponse(
        sql=out.get("sql", ""),
        result=out.get("result", ""),
        error=out.get("error", ""),
    )