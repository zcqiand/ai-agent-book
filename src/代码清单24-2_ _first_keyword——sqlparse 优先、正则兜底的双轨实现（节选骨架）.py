# 摘自 code/sql-self-healer/src/sql_self_healer/guardrail.py（节选关键骨架）
def _first_keyword(sql: str) -> str:
    """返回 SQL 首个关键字（大写）；无法解析时返回空串。"""
    sql = (sql or "").strip()
    if not sql:
        return ""
    # 主路径：sqlparse 遍历 token 流，取第一个 Keyword/DML/DDL token。
    try:
        for tok in sqlparse.parse(sql)[0].tokens:
            if tok.is_keyword or (tok.ttype is not None and "Keyword" in str(tok.ttype)):
                if kw := tok.value.strip().upper():
                    return kw
    except Exception:  # noqa: BLE001 - 解析失败时退回正则兜底
        pass
    # 兜底：正则 _FIRST_KEYWORD_RE 直接抠语句开头的第一个单词。
    match = _FIRST_KEYWORD_RE.match(sql)
    return match.group(1).upper() if match else ""