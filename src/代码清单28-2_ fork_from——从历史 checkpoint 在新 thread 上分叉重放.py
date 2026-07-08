# 摘自 code/saas-cs-agent/src/saas_cs_agent/time_travel.py
def fork_from(
    graph: Any,
    checkpoint_id: str,
    new_input: dict,
    fork_thread_id: str,
) -> dict:
    """从历史 checkpoint 起在新 thread 上分叉重放。

    构造 ``config = {"configurable": {"thread_id": fork_thread_id,
    "checkpoint_id": checkpoint_id}}``，以 ``new_input`` 调用
    ``graph.invoke``。新轨迹运行在独立的 ``fork_thread_id`` 下，与原
    thread 隔离、互不影响。

    Parameters
    ----------
    graph:
        已绑定 checkpointer 的 CompiledGraph。
    checkpoint_id:
        要回溯到的历史 checkpoint（取自 ``list_history`` 中某快照的
        ``config["configurable"]["checkpoint_id"]``）。
    new_input:
        用于驱动分叉执行的全新输入（覆盖该 checkpoint 处的状态）。
    fork_thread_id:
        分叉轨迹使用的独立线程键。

    Returns
    -------
    dict
        ``graph.invoke(new_input, config)`` 的最终状态。
    """
    config = {
        "configurable": {
            "thread_id": fork_thread_id,
            "checkpoint_id": checkpoint_id,
        }
    }
    return graph.invoke(new_input, config)