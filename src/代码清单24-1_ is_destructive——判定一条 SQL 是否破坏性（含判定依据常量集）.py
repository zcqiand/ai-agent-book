# 摘自 code/sql-self-healer/src/sql_self_healer/guardrail.py
# 永远高危的语句首关键字（大小写无关）。
_ALWAYS_DESTRUCTIVE = {"DROP", "TRUNCATE"}
# 受 WHERE 保护的有害写操作关键字。
_CONDITIONAL_WRITE = {"DELETE", "UPDATE"}
# 所有写操作关键字（用于 classify 的 write 归类）。
_WRITE_STMTS = {"INSERT", "UPDATE", "DELETE"}

# 匹配独立的 WHERE 关键字（词边界，避免命中列名/别名）。
_WHERE_RE = re.compile(r"\bWHERE\b", re.IGNORECASE)
# 兜底：直接匹配语句首个关键字（sqlparse 不可用或解析异常时）。
_FIRST_KEYWORD_RE = re.compile(r"^\s*([A-Za-z]+)")


def is_destructive(sql: str) -> bool:
    """判断 SQL 是否高危。

    - ``DROP``/``TRUNCATE`` —— 永远 True。
    - ``DELETE``/``UPDATE`` —— 无 WHERE 子句时 True，有 WHERE 时 False。
    - 其余（``SELECT``/``INSERT`` 等）—— False。
    """
    kw = _first_keyword(sql)
    if kw in _ALWAYS_DESTRUCTIVE:
        return True
    if kw in _CONDITIONAL_WRITE:
        # DELETE/UPDATE 是否带 WHERE：用正则检测整条语句。
        return _WHERE_RE.search(sql or "") is None
    return False