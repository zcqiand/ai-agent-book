# 摘自 code/sql-self-healer/src/sql_self_healer/graph.py —— should_retry 的 human 分支
def should_retry(state: AgentState) -> str:
    """``execute_sql`` 之后的条件路由函数。

    返回三态之一：

    - ``"human"``：高危 SQL 且未审批 → 等人工介入（``END``）。
    - ``"retry"``：有报错且 ``retries < MAX_RETRIES`` → 进反思重写。
    - ``"end"``：成功，或重试预算耗尽。
    """
    if is_destructive(state["sql"]) and not state["approved"]:
        return "human"
    # ... 其余 retry / end 分支（ch23 代码清单23-4 已贴整段）