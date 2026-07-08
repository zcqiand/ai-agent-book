# 摘自 code/sql-self-healer/src/sql_self_healer/nodes.py
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
        # 安全判定：高危且未审批时跳过执行——判定逻辑第24章详讲
        return {"result": "", "error": ""}

    engine = create_engine(db_url)  # 每次执行新建引擎，finally 里 dispose 防泄漏
    try:
        with engine.connect() as conn:
            result = conn.execute(text(state["sql"]))  # text() 包裹：SQLAlchemy 2.0 风格
            if not result.returns_rows:
                # DDL/无返回行 DML（DROP/CREATE/无 WHERE 的 DELETE 等）：在
                # SQLAlchemy 2.0 下 result.mappings() 会抛「does not return rows」，
                # 故先用 returns_rows 分流——显式 commit 让改动落库，再以 (no rows)
                # 成功态返回，避免被 except 当成伪错误、误触重试循环。
                conn.commit()
                return {"result": "(no rows)", "error": ""}
            rows = result.mappings().all()             # mappings().all() 取行成 dict

        if not rows:
            return {"result": "(no rows)", "error": ""}

        # 列名来自第一行的映射键，顺序与首行一致。
        columns = list(rows[0].keys())
        lines = ["\t".join(str(c) for c in columns)]   # 首行：列名（表头）
        for row in rows:
            lines.append("\t".join(str(row[c]) for c in columns))  # 后续行：值，TSV 格式化
        return {"result": "\n".join(lines), "error": ""}
    except SQLAlchemyError as exc:
        # 捕错不抛——把错误塞进 error 字段，交给 should_retry 决定 retry 还是 end
        return {"result": "", "error": str(exc)}
    finally:
        engine.dispose()  # 无论成功失败都释放引擎，避免连接泄漏