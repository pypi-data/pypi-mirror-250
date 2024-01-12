import duckdb


def get_sql_qry(filename: str, raw: bool = False) -> str:
    with open(filename, "r") as f:
        text = f.read()
    if not raw:
        for schema in ("landing", "staging", "curated", "analytics"):
            text = text.replace(f"${schema}_", f"{schema}.")

    return text


duckdb.create_function("get_sql_qry", get_sql_qry)
res = duckdb.sql(
    "SELECT get_sql_qry('../../DataPipelines/datanym/assets/IRS527/sql_scripts/staging_form8871_eain.sql', false)"
).fetchall()
print(print(res[0]))
