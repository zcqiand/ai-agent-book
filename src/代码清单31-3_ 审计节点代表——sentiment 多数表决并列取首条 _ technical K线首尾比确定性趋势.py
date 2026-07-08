# 摘自 code/quant-sentiment-research/src/quant_sentiment/nodes.py
def technical_node(state: dict, llm: Any, cache_dir: str | None = None) -> dict:
    """技术面审计。

    拉取最近 30 个交易日 K 线，比较末位 vs 首位收盘价，给出趋势（上行/下行），
    并把该论断作为一条证据入链。``llm`` 参数为接口对齐保留（本节点为确定性计算，
    不调用 LLM）。
    """
    del llm  # 接口对齐：技术面是确定性计算，不消费 LLM
    df = fetch_kline(state["symbol"], days=30, cache_dir=cache_dir)
    closes = df["close"].tolist()
    trend = "上行" if closes[-1] > closes[0] else "下行"
    # 末位日期作为证据时间戳；缺 date 列则留空
    ts = ""
    if "date" in df.columns and len(df) > 0:
        ts = str(df["date"].iloc[-1])
    partial = attach_evidence(
        state,
        claim=f"技术面：近期价格{trend}",
        source_text=f"kline closes: {closes}",
        source_url="internal:kline",
        ts=ts,
    )
    scores = dict(state.get("scores", {}))
    scores["technical"] = trend
    partial["scores"] = scores
    return partial


def sentiment_node(state: dict, llm: Any, cache_dir: str | None = None) -> dict:
    """舆情面审计。

    逐条新闻调 ``score_sentiment`` 打分，聚合出整体情绪标签
    （多/空票数相同时取首条，避免随机性）。整体标签作为一条证据入链。
    """
    news = fetch_news(state["symbol"], cache_dir=cache_dir)
    if not news:
        aggregate_label = "中性"
        source_text = ""
        source_url = "internal:news-empty"
        ts = ""
    else:
        scores_list = [score_sentiment(item, llm) for item in news]
        # 多数表决；并列时取首条标签，保证可复现
        counts: dict[str, int] = {}
        for s in scores_list:
            counts[s.label] = counts.get(s.label, 0) + 1
        top_count = max(counts.values())
        top_labels = [lbl for lbl, c in counts.items() if c == top_count]
        aggregate_label = top_labels[0] if len(top_labels) == 1 else scores_list[0].label
        first = news[0]
        source_text = str(first.get("title", ""))
        source_url = str(first.get("url", "")) or "internal:news"
        ts = str(first.get("ts", "")) if first.get("ts") else ""

    partial = attach_evidence(
        state,
        claim=f"舆情：{aggregate_label}",
        source_text=source_text,
        source_url=source_url,
        ts=ts,
    )
    scores = dict(state.get("scores", {}))
    scores["sentiment"] = aggregate_label
    partial["scores"] = scores
    return partial