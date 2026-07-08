# 摘自 code/saas-cs-agent/src/saas_cs_agent/checkpoint.py
import contextlib

_DEFAULT_SQLITE_PATH = "checkpoints.db"
# 进程级 ExitStack：持有所有已建 saver 的上下文，使底层 sqlite3 连接常驻，
# 直到调用方显式 close_all() 或解释器退出。本仓测试进程生命周期短，
# 通常无需手动关闭。
_stack: contextlib.ExitStack | None = None


def _get_stack() -> contextlib.ExitStack:
    global _stack
    if _stack is None:
        _stack = contextlib.ExitStack()
    return _stack


def close_all() -> None:
    """关闭所有由 ``make_checkpointer`` 创建的 saver 及其底层连接。

    通常只在长驻进程的优雅停机阶段调用；测试进程可不调用。
    """
    global _stack
    if _stack is not None:
        _stack.close()
        _stack = None