# ram_loader.py
import duckdb
import json
from pathlib import Path

DB_PATH = "C:/real_memory_system/memory.duckdb"
RAM_CACHE_PATH = Path("C:/real_memory_system/cache/ram_fragments.json")
RAM_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)

def load_top_fragments(tags=None, sub=None, keywords=None, limit=10000):
    conn = duckdb.connect(DB_PATH)
    conn.execute("PRAGMA enable_external_access=true")

    base = "SELECT id, claim, tags, sub_category, timestamp, content FROM fragments WHERE 1=1"
    clauses = []

    if tags:
        for tag in tags:
            clauses.append(f"array_contains(tags, '{tag}')")
    if sub:
        clauses.append(f"sub_category = '{sub}'")
    if keywords:
        for kw in keywords:
            clauses.append(f"(claim ILIKE '%{kw}%' OR content ILIKE '%{kw}%')")

    if clauses:
        base += " AND " + " AND ".join(clauses)

    base += f" ORDER BY timestamp DESC LIMIT {limit}"
    results = conn.execute(base).fetchall()
    conn.close()

    payload = [
        {
            "id": r[0],
            "claim": r[1],
            "tags": r[2],
            "sub": r[3],
            "timestamp": r[4].isoformat(),  # 🔧 fixed datetime serialization
            "content": r[5]
        }
        for r in results
    ]

    with open(RAM_CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"✅ RAM cache loaded with {len(payload)} fragments.")

if __name__ == "__main__":
    load_top_fragments()
