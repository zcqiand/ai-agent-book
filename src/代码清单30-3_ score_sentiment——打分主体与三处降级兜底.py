# 摘自 code/quant-sentiment-research/src/quant_sentiment/sentiment.py
def _build_prompt(news_item: dict) -> str:
    title = news_item.get("title", "")
    content = news_item.get("content", "")
    return (
        "你是 A 股舆情分析助手。请判断下列新闻对相关上市公司的情绪倾向。\n"
        "只返回一个 JSON 对象，不要附带任何解释或 Markdown 代码块。\n"
        '格式：{"label":"利好|利空|中性","confidence":0.0到1.0之间的浮点数}\n\n'
        f"新闻标题：{title}\n"
        f"新闻正文：{content}\n"
    )


def score_sentiment(news_item: dict, llm: _LLMLike) -> SentimentScore:
    """对单条新闻打情绪分。

    解析或校验失败时返回 ``SentimentScore(label="中性", confidence=0.3)``。
    """
    prompt = _build_prompt(news_item)
    try:
        raw = llm.generate(prompt)
    except Exception:
        return _FALLBACK.model_copy(update={"evidence_ref": news_item.get("url", news_item.get("title", ""))})

    candidate = _extract_json_object(_strip_code_fence(raw))
    try:
        data = json.loads(candidate)
    except (json.JSONDecodeError, TypeError):
        return _FALLBACK.model_copy(update={"evidence_ref": news_item.get("url", news_item.get("title", ""))})

    try:
        score = SentimentScore.model_validate(data)
    except ValidationError:
        return _FALLBACK

    # 补全证据引用（LLM 通常不主动返回）
    if not score.evidence_ref:
        score = score.model_copy(
            update={"evidence_ref": news_item.get("url", news_item.get("title", ""))}
        )
    return score