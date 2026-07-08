# 跑 test_graph.py：用 tmp_path 现造 fixture + FakeLLM 顶替 LLM，验证多波次审计全链
cd code/quant-sentiment-research
pytest tests/test_graph.py -v