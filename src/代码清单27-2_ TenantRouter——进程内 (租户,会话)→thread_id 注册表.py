# 摘自 code/saas-cs-agent/src/saas_cs_agent/tenant.py
class TenantRouter:
    """进程内的 (租户, 会话) → thread_id 注册表。

    ``register`` 为一对 (租户, 会话) 显式登记一个 ``thread_id``（由
    :func:`thread_id_for` 生成）并返回；``get_thread`` 优先返回已登记的
    值，若该组合从未登记则即时构建一个（保证调用方总能拿到稳定的
    ``thread_id``，不因登记顺序差异而漂移）。
    """

    def __init__(self) -> None:
        # 内部映射：(tenant_id, session_id) -> thread_id
        self._threads: dict[tuple[str, str], str] = {}

    def register(self, tenant_id: str, session_id: str) -> str:
        """登记并返回 (租户, 会话) 的 thread_id。

        重复登记同一组合是幂等的：始终返回由 :func:`thread_id_for` 派生
        的同一值（格式确定，无随机性）。
        """
        tid = thread_id_for(tenant_id, session_id)
        self._threads[(tenant_id, session_id)] = tid
        return tid

    def get_thread(self, tenant_id: str, session_id: str) -> str:
        """返回 (租户, 会话) 的 thread_id。

        已登记则返回存储值；未登记则即时构建并返回（不写入注册表，
        保持 ``register`` 的显式语义）。
        """
        stored = self._threads.get((tenant_id, session_id))
        if stored is not None:
            return stored
        return thread_id_for(tenant_id, session_id)