# 摘自 code/sql-self-healer/src/sql_self_healer/schema.py
def get_sample_data(db_url: str, table: str, n: int = 3) -> list[dict]:
    engine = create_engine(db_url)
    try:
        with engine.connect() as conn:
            # SQLAlchemy 2.0 style：text() 包裸 SQL，mappings().all() 把行转成可读 dict
            result = conn.execute(text(f"SELECT * FROM {table} LIMIT {n}"))
            rows = [dict(row) for row in result.mappings().all()]
        return rows
    finally:
        engine.dispose()