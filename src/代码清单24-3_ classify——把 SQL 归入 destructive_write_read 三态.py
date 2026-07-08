# 摘自 code/sql-self-healer/src/sql_self_healer/guardrail.py
def classify(sql: str) -> str:
    """把 SQL 归类为 ``destructive`` / ``write`` / ``read``。

    - 高危语句（见 ``is_destructive``）→ ``"destructive"``。
    - 其余 INSERT/UPDATE/DELETE → ``"write"``。
    - SELECT（及任何非写操作）→ ``"read"``。
    """
    if is_destructive(sql):
        return "destructive"
    kw = _first_keyword(sql)
    if kw in _WRITE_STMTS:
        return "write"
    return "read"