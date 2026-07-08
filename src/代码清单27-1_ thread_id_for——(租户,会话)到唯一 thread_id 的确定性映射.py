# 摘自 code/saas-cs-agent/src/saas_cs_agent/tenant.py
def thread_id_for(tenant_id: str, session_id: str) -> str:
    """返回 (租户, 会话) 对应的唯一 thread_id。

    格式 ``"{tenant_id}:{session_id}"``：可读、可解析，且天然保证
    不同租户或不同会话得到不同的 ``thread_id``。
    """
    return f"{tenant_id}:{session_id}"