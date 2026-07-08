# 摘自 code/quant-sentiment-research/src/quant_sentiment/grounding.py
def validate_report(state: dict) -> bool:
    """防幻觉门控。

    - 报告非空（有结论）但证据数为 0 → 拒绝（False）
    - 报告为空，或报告背后有 ≥1 条证据 → 通过（True）
    """
    if state.get("report") and len(state.get("evidence", [])) == 0:
        return False
    return True