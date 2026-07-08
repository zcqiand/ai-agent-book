# 摘自 code/sql-self-healer/src/sql_self_healer/api.py
def get_llm():
    """LLM 依赖工厂：默认走 ``make_llm``（无 Key 时返回 FakeLLM）。"""
    return make_llm()