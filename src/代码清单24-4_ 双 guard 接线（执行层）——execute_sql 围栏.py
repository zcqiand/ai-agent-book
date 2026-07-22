# 摘自 code/sql-self-healer/src/sql_self_healer/nodes.py —— execute_sql 的安全围栏
def execute_sql(state: AgentState, db_url: str) -> dict:
    """执行 ``state["sql"]``，返回结果行或报错信息。

    成功：``{"result": <格式化后的行字符串>, "error": ""}``。
    抛 ``SQLAlchemyError``：``{"result": "", "error": <str(exc)>}``。
    引擎无论成败都会 ``dispose``。

    安全围栏：当 ``is_destructive(state["sql"]) and not state["approved"]``
    时**跳过执行**——返回 ``{"result": "", "error": ""}``，让路由节点
    ``should_retry`` 把流程引向 ``"human"``（人工审批），从而保证一条未授权的
    ``DROP`` 永远不会真正落到数据库上。
    """
    if is_destructive(state["sql"]) and not state.get("approved", False):
        return {"result": "", "error": ""}
    # ... 其余执行逻辑（ch23 代码清单23-3 已贴整段）