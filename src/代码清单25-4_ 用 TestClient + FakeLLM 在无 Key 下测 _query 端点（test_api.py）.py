# 摘自 code/sql-self-healer/tests/test_api.py
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from sql_self_healer.api import app, get_llm
from sql_self_healer.llm import FakeLLM


def test_query_endpoint(tmp_path):
    db = f"sqlite:///{tmp_path}/t.db"
    eng = create_engine(db)
    with eng.connect() as c:
        c.execute(text("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"))
        c.execute(text("INSERT INTO users (id, name) VALUES (1, 'alice')"))
        c.commit()
    eng.dispose()

    app.dependency_overrides[get_llm] = lambda: FakeLLM(script=["SELECT * FROM users"])
    try:
        client = TestClient(app)
        resp = client.post(
            "/query",
            json={"query": "列出用户", "tenant_id": "t1", "db_url": db},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["sql"]  # non-empty
        assert "alice" in body["result"]
        assert body["error"] == ""
    finally:
        app.dependency_overrides.clear()