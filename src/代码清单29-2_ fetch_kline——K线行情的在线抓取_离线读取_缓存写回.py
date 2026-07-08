# 摘自 code/quant-sentiment-research/src/quant_sentiment/gateway.py

def fetch_kline(symbol: str, days: int = 30, cache_dir: str | None = None):
    """取 ``symbol`` 最近 ``days`` 个交易日的 K 线。

    - 离线模式（``set_offline(True)`` 或 akshare 不可导入）：从
      ``{cache_dir}/kline_{symbol}.parquet`` 读取，缺失则抛
      ``FileNotFoundError`` 并给出清晰提示。
    - 在线模式：调用 akshare 取近期日 K，返回含 ``close`` 列的 DataFrame；
      若给定 ``cache_dir`` 则写回 parquet 供离线复用。

    返回的 DataFrame 至少含 ``close`` 列。
    """
    import pandas as pd  # 懒加载：测试外不必强依赖

    if _offline_active():
        if not cache_dir:
            raise FileNotFoundError(
                f"离线模式下需要 cache_dir 来定位 kline_{symbol}.parquet"
            )
        path = _kline_cache_path(cache_dir, symbol)
        try:
            df = pd.read_parquet(path)
        except FileNotFoundError as exc:  # pragma: no cover - 路径已校验
            raise FileNotFoundError(
                f"离线 K 线 fixture 缺失：{path}；请先在线抓取或补 fixture"
            ) from exc
        if "close" not in df.columns:
            raise ValueError(f"离线 K 线 fixture {path} 缺少 close 列")
        return df.tail(days).reset_index(drop=True)

    # 在线：akshare 已在 _offline_active() 中确认可导入
    import akshare as ak

    df = ak.stock_zh_a_hist(
        symbol=symbol, period="daily", adjust="qfq"
    )
    # akshare 返回中文列名，统一映射到英文 close
    if "close" not in df.columns and "收盘" in df.columns:
        df = df.rename(columns={"收盘": "close"})
    if "close" not in df.columns:
        raise ValueError(f"akshare 返回的 K 线缺少 close 列：{list(df.columns)}")
    df = df.tail(days).reset_index(drop=True)
    if cache_dir:
        import os

        os.makedirs(cache_dir, exist_ok=True)
        df.to_parquet(_kline_cache_path(cache_dir, symbol), index=False)
    return df