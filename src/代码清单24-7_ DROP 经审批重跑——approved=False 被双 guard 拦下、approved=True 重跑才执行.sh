# 在 code/sql-self-healer 目录下执行；PYTHONPATH=src 保证可导入包内模块
cd code/sql-self-healer
$env:PYTHONPATH="src"   # PowerShell 写法；bash 用 export PYTHONPATH=src
python -c "import tempfile, os; \
from sqlalchemy import create_engine, text; \
from sql_self_healer.llm import FakeLLM; \
from sql_self_healer.graph import build_graph; \
db='sqlite:///'+os.path.join(tempfile.mkdtemp(),'t.db'); \
eng=create_engine(db); \
c=eng.connect(); \
c.execute(text('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)')); \
c.execute(text(\"INSERT INTO users VALUES (1,'alice')\")); c.commit(); c.close(); \
print('--- 第一步：approved=False，DROP 应被双 guard 拦下，走 human，表还在 ---'); \
g=build_graph(llm=FakeLLM(script=['DROP TABLE users']), db_url=db); \
out=g.invoke({'query':'清掉 users 表','sql':'','error':'','retries':0,'result':'','tenant_id':'t1','approved':False}); \
print('error=',repr(out['error'])); \
with eng.connect() as chk: \
    leftover=chk.execute(text(\"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='users'\")).scalar(); \
    print('users 表是否仍在(1=在/0=没):', leftover); \
print('--- 第二步：人审通过，approved=True 写回，重跑——围栏不再命中，DROP 执行 ---'); \
out2=g.invoke({'query':'清掉 users 表','sql':'','error':'','retries':0,'result':'','tenant_id':'t1','approved':True}); \
print('error=',repr(out2['error'])); \
with eng.connect() as chk2: \
    gone=chk2.execute(text(\"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='users'\")).scalar(); \
    print('users 表是否还在(1=在/0=没):', gone)"
# 预期输出：
#   --- 第一步：approved=False，DROP 应被双 guard 拦下，走 human，表还在 ---
#   error= ''
#   users 表是否仍在(1=在/0=没): 1        ← execute_sql 围栏跳过、should_retry 路由 human→END，DROP 没落库
#   --- 第二步：人审通过，approved=True 写回，重跑——围栏不再命中，DROP 执行 ---
#   error= ''
#   users 表是否还在(1=在/0=没): 0        ← is_destructive(...) and not approved 因 approved=True 不再命中，DROP 真正执行；execute_sql 内 result.returns_rows 守卫把不返回行的 DDL 分流到 (no rows) 成功态（清单23-3），故 error 为空、不再误触 retry