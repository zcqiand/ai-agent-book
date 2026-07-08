# 手动造最小 fixture + FakeLLM，invoke 一次看简报与证据累加
cd code/quant-sentiment-research
python -c "
import json, tempfile, os
import pandas as pd
from quant_sentiment.gateway import set_offline
from quant_sentiment.graph import build_graph
from quant_sentiment.llm import FakeLLM  # ch30 _LLMLike Protocol 的 FakeLLM 实现

# 造离线 fixture（沿用 ch29 网关约定：kline_*.parquet 至少含 close 列，news_*.json 是 list[{title,content,url,ts?}]）
d = tempfile.mkdtemp()
pd.DataFrame({'date': ['2026-01-01', '2026-01-02'], 'close': [10.0, 10.5]}).to_parquet(os.path.join(d, 'kline_600000.parquet'))
with open(os.path.join(d, 'news_600000.json'), 'w', encoding='utf-8') as f:
    json.dump([{'title': '业绩超预期', 'content': 'Q1营收大增', 'url': 'http://x/1', 'ts': '2026-01-02'}], f)

set_offline(True)  # 切离线，走本地 fixture
g = build_graph(FakeLLM(script=['{\"label\":\"利好\",\"confidence\":0.8}']), cache_dir=d)
out = g.invoke({'symbol': '600000', 'evidence': [], 'scores': {}, 'report': '', 'model_tier': 'lite'})
print(out['report'])
print('evidence 条数:', len(out['evidence']))
"