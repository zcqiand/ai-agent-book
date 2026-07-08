# 摘自 code/sql-self-healer/src/sql_self_healer/schema.py
def load_schema(db_url: str) -> str:
    engine = create_engine(db_url)
    try:
        # 用 inspect 而非硬编码 DDL：库会演进，内省才能保证 schema 描述与真实结构始终一致
        insp = inspect(engine)
        table_names = insp.get_table_names()

        parts: list[str] = []
        if not table_names:
            return "Database has no tables."

        parts.append(f"Database tables ({len(table_names)}):")
        for table in table_names:
            parts.append(f"\n## Table: {table}")
            columns = insp.get_columns(table)
            # SQLAlchemy 2.0 中 get_pk_constraint 返回字典的标准 key 是
            # constrained_columns（实测 {'constrained_columns': ['id'], ...}）。
            # 主键集合用于给列打 [PK] 标记，帮 LLM 识别表的唯一标识列
            pk_cols = set(insp.get_pk_constraint(table).get("constrained_columns", []) or [])

            parts.append("Columns:")
            for col in columns:
                pk_marker = " [PK]" if col["name"] in pk_cols else ""
                # SQLite 反射 INTEGER PRIMARY KEY 时 nullable=True（方言怪癖），
                # 对读者反直觉；主键在语义上必须 NOT NULL，这里强制纠正显示
                is_pk = col["name"] in pk_cols or col.get("primary_key")
                nullable = "NOT NULL" if is_pk else ("NULL" if col.get("nullable", True) else "NOT NULL")
                col_type = str(col.get("type", "UNKNOWN"))
                parts.append(
                    f"  - {col['name']}: {col_type} {nullable}{pk_marker}"
                )

            # 样例数据让 LLM 不只看到字段类型，还能看到字段实际取值的形态
            sample = get_sample_data(db_url, table, n=3)
            if sample:
                parts.append(f"Sample rows ({len(sample)}):")
                for row in sample:
                    parts.append(f"  {row}")
            else:
                parts.append("Sample rows: (empty table)")

        return "\n".join(parts)
    finally:
        engine.dispose()