# 摘自 code/sql-self-healer/src/sql_self_healer/nodes.py
from __future__ import annotations

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from .guardrail import is_destructive
from .schema import load_schema
from .state import AgentState


def generate_sql(state: AgentState, llm, db_url: str) -> dict:
    """调用 LLM 把自然语言查询翻译成 SQL。

    提示词注入 ``load_schema(db_url)`` 反射出的表结构与样例数据，
    以及用户的自然语言 ``state["query"]``，再交给 ``llm.generate``
    产出可执行 SQL。

    返回部分状态 ``{"sql": <LLM 输出>}``。
    """
    schema = load_schema(db_url)  # 接地（承接 ch22）：把真实表结构喂给 LLM，压住结构性幻觉
    prompt = (
        "You are a SQL expert. Given the database schema below and a "
        "natural-language question, output ONLY the single SQL statement "
        "that answers the question — no markdown, no explanation.\n\n"
        f"### SCHEMA\n{schema}\n\n"
        f"### QUESTION\n{state['query']}\n\n"
        "### SQL\n"
    )
    sql = llm.generate(prompt)
    return {"sql": sql}  # 只返回变更字段，LangGraph 合并写回 AgentState


# ---------- 上面是「生成」，下面是「反思重写」----------


def reflect_and_rewrite(state: AgentState, llm) -> dict:
    """把执行报错反馈给 LLM，生成修正后的 SQL。

    提示词包含失败的 SQL 与报错信息，要求 LLM 输出修复版本。
    返回 ``{"sql": <新 SQL>, "retries": state["retries"] + 1}``。
    """
    prompt = (
        "The following SQL failed with the given error. Output ONLY the "
        "corrected SQL — no markdown, no explanation.\n\n"
        f"### FAILED SQL\n{state['sql']}\n\n"   # 上一轮失败的 SQL 原样喂回
        f"### ERROR\n{state['error']}\n\n"      # 执行器捕到的报错（自愈的关键反馈）
        "### CORRECTED SQL\n"
    )
    sql = llm.generate(prompt)
    # retries+1 让 should_retry 知道还剩多少预算——这是终止性的计数基础
    return {"sql": sql, "retries": state["retries"] + 1}