# 摘自 code/quant-sentiment-research/src/quant_sentiment/grounding.py
def attach_evidence(
    state: dict,
    claim: str,
    source_text: str,
    source_url: str,
    ts: str,
) -> dict:
    """构建 Evidence 并返回 partial state（仅含 evidence 键），不修改输入 state。

    用法（LangGraph node 中）::

        return attach_evidence(state, claim, src, url, ts)

    返回的 dict 会与上游 state 做浅合并，从而把新证据累加到 state["evidence"]。
    """
    ev = Evidence(
        claim=claim,
        source_text=source_text,
        source_url=source_url,
        ts=ts,
    )
    return {"evidence": state.get("evidence", []) + [ev]}