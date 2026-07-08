# 摘自 code/sql-self-healer/src/sql_self_healer/state.py
"""LangGraph 全局状态定义。

``AgentState`` 在各节点间传递：自然语言查询、生成的 SQL、执行报错、
重试次数、查询结果、租户隔离标识、人工审批标志。
"""

from __future__ import annotations

from typing import TypedDict


class AgentState(TypedDict):
    """Agent 各节点共享的全局状态。"""

    query: str       # 自然语言查询
    sql: str         # 当前 SQL（每轮可能被反思节点改写）
    error: str       # 执行报错——自愈循环的触发信号
    retries: int     # 已重试次数——与 MAX_RETRIES 一起保证终止
    result: str      # 查询结果（TSV 文本或 "(no rows)"）
    tenant_id: str   # 租户隔离标识
    approved: bool   # 人工审批标志——高危语句走 human 分支的前提