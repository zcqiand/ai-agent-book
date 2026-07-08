# 摘自 code/quant-sentiment-research/src/quant_sentiment/sentiment.py
"""舆情情绪打分器。

输入一条新闻（``{title, content?, url?, ts?}``），用 LLM 判定其对
A股标的的情绪倾向（利好 / 利空 / 中性）并给出置信度。

设计要点：
- 用 pydantic 校验 LLM 返回的 JSON，避免脏数据污染下游。
- 任何解析/校验失败都降级为低置信度的「中性」，绝不抛异常打断流水线
  ——后续 grounding 节点会据此把证据强度下调。
"""

from __future__ import annotations

import json
import re
from typing import Literal, Protocol

from pydantic import BaseModel, ValidationError


class _LLMLike(Protocol):
    """最小 LLM 接口（FakeLLM 与真实 ChatModel 适配器都满足）。"""

    def generate(self, prompt: str) -> str: ...


class SentimentScore(BaseModel):
    """单条新闻的情绪判定结果。

    - ``label``：利好 / 利空 / 中性。
    - ``confidence``：0.0~1.0，模型自报的置信度。
    - ``evidence_ref``：可追溯的证据引用（新闻 url 或标题），供后续证据链使用。
    """

    label: Literal["利好", "利空", "中性"]
    confidence: float
    evidence_ref: str = ""


_FALLBACK = SentimentScore(label="中性", confidence=0.3)