# 摘自 code/quant-sentiment-research/src/quant_sentiment/nodes.py
def summarize_node(state: dict) -> dict:
    """综述节点：把 symbol + 三维评分 + 证据数拼成一段研究简报。

    报告**只做事实陈述**，不含任何买卖建议。``validate_report`` 在证据已挂载
    的前提下恒为 True——审计节点在前序波次已写入证据链。
    """
    symbol = state.get("symbol", "")
    scores = state.get("scores", {})
    evidence = state.get("evidence", [])
    technical = scores.get("technical", "未知")
    fund_flow = scores.get("fund_flow", "未知")
    sentiment = scores.get("sentiment", "未知")

    report = (
        f"标的 {symbol} 多波次审计简报："
        f"技术面 {technical}；资金面 {fund_flow}；舆情 {sentiment}；"
        f"证据 {len(evidence)} 条。"
        f"（本简报仅陈述研究事实，不构成任何投资建议。）"
    )
    new_state = dict(state)
    new_state["report"] = report
    # 防幻觉门控：审计节点已挂证据，此处恒为 True；保持防御性断言
    assert validate_report(new_state) is True, "综述阶段证据缺失，违反 grounding 门控"
    return {"report": report}