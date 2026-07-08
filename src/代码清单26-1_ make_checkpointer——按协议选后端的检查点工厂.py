# 摘自 code/saas-cs-agent/src/saas_cs_agent/checkpoint.py
def make_checkpointer(db_path: str = _DEFAULT_SQLITE_PATH):
    """创建并返回一个 checkpointer 实例。

    Parameters
    ----------
    db_path:
        - 默认 ``"checkpoints.db"`` 或任意文件路径 / ``sqlite://`` 前缀 →
          返回 ``SqliteSaver``。
        - 以 ``postgresql://`` 开头 → 尝试返回 ``PostgresSaver``；若
          ``langgraph-checkpoint-postgres`` 未安装则抛出带提示的 ``ImportError``。

    Returns
    -------
    BaseCheckpointSaver
        已初始化、底层连接保持打开的 saver 实例。**调用方拥有其生命周期**——
        进程退出前应调用 :func:`close_all`（或自行管理）以释放连接。

    Notes
    -----
    ``SqliteSaver.from_conn_string`` 是一个上下文管理器风格的工厂（在
    langgraph 1.2.x / langgraph-checkpoint-sqlite 2.x+ 中返回
    ``Iterator[SqliteSaver]``）。这里通过一个进程级 ``ExitStack`` 进入其
    上下文、取出它 yield 出来的 saver，并让连接在进程生命周期内常驻。
    """
    if db_path.startswith("postgresql://"):
        try:
            from langgraph.checkpoint.postgres import PostgresSaver  # type: ignore[import-not-found]
        except ImportError as exc:  # pragma: no cover - 取决于可选依赖是否安装
            raise ImportError(
                "需要 'langgraph-checkpoint-postgres' 才能使用 PostgresSaver。"
                "请运行 `pip install langgraph-checkpoint-postgres`，或改用 SQLite（默认）。"
            ) from exc
        # PostgresSaver 同样是上下文管理器风格工厂；按需实例化。
        return _enter_context(PostgresSaver.from_conn_string(db_path))

    # SQLite 路径（默认）
    from langgraph.checkpoint.sqlite import SqliteSaver

    return _enter_context(SqliteSaver.from_conn_string(db_path))


def _enter_context(factory: Iterator):
    """进入一个上下文管理器风格的工厂，返回其产物，并由进程级栈保活。"""
    stack = _get_stack()
    return stack.enter_context(factory)