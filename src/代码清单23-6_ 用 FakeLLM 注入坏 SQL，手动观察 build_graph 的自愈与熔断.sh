# 在 code/sql-self-healer 目录下执行；PYTHONPATH=src 保证可导入包内模块
cd code/sql-self-healer
$env:PYTHONPATH="src"   # bash 用 export PYTHONPATH=src
python -c "import tempfile, os; \
from sqlalchemy import create_engine, text; \
from sql_self_healer.llm import FakeLLM; \
from sql_self_healer.graph import build_graph; \
db='sqlite:///'+os.path.join(tempfile.mkdtemp(),'t.db'); \
eng=create_engine(db); \
c=eng.connect(); c.execute(text('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)')); c.execute(text(\"INSERT INTO users VALUES (1,'alice')\")); c.commit(); c.close(); \
g=build_graph(llm=FakeLLM(script=['SELECT bad_col FROM users','SELECT * FROM users']), db_url=db); \
out=g.invoke({'query':'列出用户','sql':'','error':'','retries':0,'result':'','tenant_id':'t1','approved':True}); \
print('retries=',out['retries']); print('result=',out['result']); print('error=',repr(out['error']))"
# 第一条 SQL 字段名错→执行报错→retry→反思重写成第二条→执行成功。观察 retries=1、result 非空、error 为空。
# 动手题一：把 FakeLLM 的 script 全改成坏 SQL（如 ['SELECT bad FROM users']*4），看 retries 涨到 MAX_RETRIES=3 后路由 end 终止。
# 动手题二：把 approved 改成 False、script 改成 ['DROP TABLE users']，观察走 human 分支：error 为空、表未被删（安全熔断）。