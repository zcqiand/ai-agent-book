# 摘自 code/sql-self-healer/src/sql_self_healer/graph.py
from __future__ import annotations

import functools

from langgraph.graph import END, START, StateGraph

from .guardrail import is_destructive
from .nodes import execute_sql, generate_sql, reflect_and_rewrite
from .state import AgentState

# 自愈循环的最大重试次数：超过即放弃，路由到 "end"。
MAX_RETRIES = 3


def should_retry(state: AgentState) -> str:
    """``execute_sql`` 之后的条件路由函数。

    返回三态之一：

    - ``"human"``：高危 SQL 且未审批 → 等人工介入（``END``）。
    - ``"retry"``：有报错且 ``retries < MAX_RETRIES`` → 进反思重写。
    - ``"end"``：成功，或重试预算耗尽。
    """
    # 三态优先级：human（安全熔断，最优先）> retry（自愈循环）> end（成功/预算耗尽）
    if is_destructive(state["sql"]) and not state["approved"]:
        return "human"
    if state["error"] and state["retries"] < MAX_RETRIES:
        return "retry"
    return "end"


def build_graph(llm, db_url: str, checkpointer=None):
    """构建并编译自愈状态机。

    用 ``functools.partial`` 把 ``llm`` / ``db_url`` 绑到节点上，使其只剩
    ``state`` 一个入参（LangGraph 节点契约）；再按拓扑连边、加条件路由，
    最后以可选 ``checkpointer`` 编译返回 ``CompiledGraph``。
    """
    graph = StateGraph(AgentState)

    # partial 绑参：节点退化成单参 state 函数（LangGraph 契约），又保留可独立测试性
    graph.add_node("generate_sql", functools.partial(generate_sql, llm=llm, db_url=db_url))
    graph.add_node("execute_sql", functools.partial(execute_sql, db_url=db_url))
    graph.add_node("reflect_and_rewrite", functools.partial(reflect_and_rewrite, llm=llm))

    graph.add_edge(START, "generate_sql")            # 入口 → 生成
    graph.add_edge("generate_sql", "execute_sql")    # 生成 → 执行（直线段）
    graph.add_conditional_edges(
        "execute_sql",
        should_retry,
        # 三态映射：retry 回头反思（构成自愈环），human/end 都收尾到 END
        {"retry": "reflect_and_rewrite", "human": END, "end": END},
    )
    graph.add_edge("reflect_and_rewrite", "execute_sql")  # 反思后重试——这条回头边围成自愈循环

    return graph.compile(checkpointer=checkpointer)