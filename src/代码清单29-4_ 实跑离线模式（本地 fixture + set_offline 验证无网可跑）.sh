# 进入案例仓
cd code/quant-sentiment-research

# 方式一：先落地一份本地 fixture（与 tests/test_gateway.py 同款），
# 再用 set_offline(True) 跑离线模式的 fetch_kline / fetch_news
python -c "import json, tempfile, os; from quant_sentiment.gateway import set_offline, fetch_kline, fetch_news; import pandas as pd; \
d = tempfile.mkdtemp(); \
pd.DataFrame({'date': ['2026-01-01','2026-01-02'], 'close': [10.0, 10.5]}).to_parquet(os.path.join(d, 'kline_600000.parquet')); \
open(os.path.join(d, 'news_600000.json'), 'w', encoding='utf-8').write(json.dumps([{'title': '示例新闻', 'content': '业绩说明会纪要', 'url': 'http://example.com'}], ensure_ascii=False)); \
set_offline(True); \
print(fetch_kline('600000', days=5, cache_dir=d)[['close']]); \
print(len(fetch_news('600000', cache_dir=d)))"

# 方式二：直接跑网关测试（仓内 17 passed，含离线 fixture 用例）
pytest tests/test_gateway.py -q