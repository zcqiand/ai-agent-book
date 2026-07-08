# 摘自 code/quant-sentiment-research/src/quant_sentiment/gateway.py

def fetch_news(symbol: str, cache_dir: str | None = None) -> list[dict[str, Any]]:
    """取 ``symbol`` 相关新闻列表。

    - 离线模式：从 ``{cache_dir}/news_{symbol}.json`` 读取。
    - 在线模式：调用 akshare 取新闻，``cache_dir`` 给定时写回 json。

    返回 ``list[dict]``，每项形如 ``{title, content, url, ts?}``。
    """
    if _offline_active():
        if not cache_dir:
            raise FileNotFoundError(
                f"离线模式下需要 cache_dir 来定位 news_{symbol}.json"
            )
        path = _news_cache_path(cache_dir, symbol)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except FileNotFoundError as exc:  # pragma: no cover - 路径已校验
            raise FileNotFoundError(
                f"离线新闻 fixture 缺失：{path}；请先在线抓取或补 fixture"
            ) from exc

    import akshare as ak

    raw = ak.stock_news_em(symbol=symbol)
    # akshare 返回 DataFrame，列名为中文；映射到统一 schema
    col_map = {"新闻标题": "title", "新闻内容": "content", "新闻链接": "url", "发布时间": "ts"}
    records: list[dict[str, Any]] = []
    for _, row in raw.iterrows():
        item = {col_map.get(c, c): row[c] for c in raw.columns}
        records.append(
            {
                "title": item.get("title", ""),
                "content": item.get("content", ""),
                "url": item.get("url", ""),
                **({"ts": item["ts"]} if "ts" in item else {}),
            }
        )
    if cache_dir:
        import os

        os.makedirs(cache_dir, exist_ok=True)
        with open(_news_cache_path(cache_dir, symbol), "w", encoding="utf-8") as fh:
            json.dump(records, fh, ensure_ascii=False)
    return records