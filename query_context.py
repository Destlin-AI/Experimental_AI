# query_context.py
import duckdb
from pathlib import Path
from datetime import datetime

DB_DIR = Path("C:/real_memory_system")
DEFAULT_LIMIT = 2048

def get_context(category, tags=None, sub=None, keywords=None, max_chars=DEFAULT_LIMIT):
    db_path = DB_DIR / f"{category}.duckdb"
    if not db_path.exists():
        raise FileNotFoundError(f"Missing DB: {db_path}")

    conn = duckdb.connect(str(db_path))
    base_query = "SELECT claim, content, tags, timestamp FROM fragments WHERE 1=1"
    clauses = []

    if sub:
        clauses.append(f"sub_category = '{sub}'")
    if tags:
        for tag in tags:
            clauses.append(f"array_contains(tags, '{tag}')")
    if keywords:
        for kw in keywords:
            clauses.append(f"(claim ILIKE '%{kw}%' OR content ILIKE '%{kw}%')")

    if clauses:
        base_query += " AND " + " AND ".join(clauses)

    base_query += " ORDER BY timestamp DESC"

    results = conn.execute(base_query).fetchall()
    context = []
    total_chars = 0

    for claim, content, tags, timestamp in results:
        block = f"# {timestamp} [{', '.join(tags)}]\n{claim}\n\n{content}\n"
        if total_chars + len(block) > max_chars:
            break
        context.append(block)
        total_chars += len(block)

    conn.close()
    return "\n".join(context)
