# 摘自 code/quant-sentiment-research/src/quant_sentiment/state.py
@dataclass
class Evidence:
    """单条证据：claim(论断) + 出处文本 + 出处 URL + 时间戳。"""

    claim: str
    source_text: str
    source_url: str
    ts: str