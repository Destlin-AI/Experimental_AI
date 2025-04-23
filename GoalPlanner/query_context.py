# query_context.py — fragment fetcher from one or multiple DuckDBs

import duckdb
from pathlib import Path

def fetch_fragments(db_path: str, tags: list[str], limit: int = 10):
    con = duckdb.connect(db_path)
    query = f"""
        SELECT id, claim, sub_category, tags, content, timestamp
        FROM fragments
        WHERE array_has_any(tags, {tags})
        ORDER BY timestamp DESC LIMIT {limit}
    """
    results = con.execute(query).fetchall()
    con.close()
    return results