# 摘自 code/quant-sentiment-research/src/quant_sentiment/state.py
class QuantState(TypedDict):
    """LangGraph 全局状态。

    - symbol:      股票代码（如 "600000"）
    - evidence:    已采集的证据链 list[Evidence]
    - scores:      各维度评分 dict（technical / fund_flow / sentiment ...）
    - report:      最终结论文本
    - model_tier:  LLM 档位（"lite" / "pro" ...）
    """

    symbol: str
    evidence: List[Evidence]
    scores: dict
    report: str
    model_tier: str