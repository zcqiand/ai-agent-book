# 在 code/sql-self-healer 目录下执行；PYTHONPATH=src 保证可导入包内模块
# PowerShell 写法
cd code/sql-self-healer
$env:PYTHONPATH="src"
pytest tests/test_api.py -v

# bash / zsh 写法
cd code/sql-self-healer
export PYTHONPATH=src
pytest tests/test_api.py -v
# 期望：POST /query 返回状态码 200、sql 非空、result 含 alice、error 为空字符串