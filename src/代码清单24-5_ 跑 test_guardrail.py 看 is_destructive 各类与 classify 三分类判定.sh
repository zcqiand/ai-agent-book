# 在 code/sql-self-healer 目录下执行；PYTHONPATH=src 保证可导入包内模块
cd code/sql-self-healer
$env:PYTHONPATH="src"   # PowerShell 写法；bash 用 export PYTHONPATH=src
pytest tests/test_guardrail.py -v
# 期望：is_destructive 各类（DROP/TRUNCATE 恒 True、无 WHERE DELETE/UPDATE True、带 WHERE False、SELECT/INSERT False）
#       与 classify 三分类（destructive/write/read）全绿