# 摘自 code/quant-sentiment-research/src/quant_sentiment/gateway.py

# 模块级离线开关。测试通过 set_offline(True) 强制走本地 fixture；
# 生产可保持 False，由 akshare 是否可导入自然降级。
_OFFLINE: bool = False


def set_offline(flag: bool) -> None:
    """切换网关离线模式。"""
    global _OFFLINE
    _OFFLINE = bool(flag)


def _offline_active() -> bool:
    """离线模式生效 = 显式开启 OR akshare 不可导入。"""
    if _OFFLINE:
        return True
    try:
        import akshare  # noqa: F401
    except Exception:
        return True
    return False