# 在 code/sql-self-healer 目录下执行。PYTHONPATH=src 让 sql_self_healer 可导入
python -c "from sqlalchemy import create_engine, text; from sql_self_healer.schema import load_schema; \
eng = create_engine('sqlite:///tmp_demo.db'); \
c = eng.connect(); \
c.execute(text('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)')); \
c.execute(text(\"INSERT INTO users (id, name) VALUES (1, 'alice'), (2, 'bob')\")); \
c.commit(); c.close(); \
print(load_schema('sqlite:///tmp_demo.db'))"