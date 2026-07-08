# 在 code/sql-self-healer 目录下执行；PYTHONPATH=src 让测试能导入 sql_self_healer 包
cd code/sql-self-healer
$env:PYTHONPATH="src"          # PowerShell 写法；bash 用 export PYTHONPATH=src
pytest tests/test_graph.py -v
# 期望：test_self_heal_loop（坏 SQL → 反思 → 改对 → 成功）/ test_destructive_routes_to_human_not_executed（DROP 走 human、表还在）全绿