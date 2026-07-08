# 摘自 code/saas-cs-agent/src/saas_cs_agent/time_travel.py
def list_history(graph: Any, thread_id: str) -> list:
    """返回某 ``thread_id`` 的历史 ``StateSnapshot`` 列表。

    直接消费 ``graph.get_state_history``，并物化为列表，方便测试取
    ``config["configurable"]["checkpoint_id"]`` 与 ``.values``。

    Parameters
    ----------
    graph:
        已绑定 checkpointer 的 CompiledGraph。
    thread_id:
        要回看的对话线程键。

    Returns
    -------
    list[StateSnapshot]
        历史快照列表，**最新在前**（与 ``get_state_history`` 的 yield
        顺序一致），因此 ``[-1]`` 是最早的 checkpoint。
    """
    return list(
        graph.get_state_history({"configurable": {"thread_id": thread_id}})
    )