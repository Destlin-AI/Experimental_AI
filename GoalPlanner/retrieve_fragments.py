# === BATCH 2: retrieve_fragments.py ===

import duckdb
import os
from pathlib import Path
from datetime import datetime

MEMORY_DIR = Path("D:/Project_AI/memory_db")

def retrieve_fragments(
    query: str,
    categories: list = None,
    top_k: int = 10,
    confidence_threshold: float = 0.5
):
    results = []
    categories = categories or [f.stem for f in MEMORY_DIR.glob("*.duckdb")]

    for cat in categories:
        db_path = MEMORY_DIR / f"{cat}.duckdb"
        if not db_path.exists():
            continue
        try:
            conn = duckdb.connect(str(db_path))
            query_stmt = f"""
                SELECT *,
                       SIMILARITY('{query}', claim) AS similarity
                FROM fragments
                WHERE confidence >= {confidence_threshold}
                ORDER BY similarity DESC
                LIMIT {top_k};
            """
            res = conn.execute(query_stmt).fetchall()
            for row in res:
                results.append({"category": cat, "row": row})
            conn.close()
        except Exception as e:
            print(f"[⚠️] Failed on {cat}: {e}")

    return sorted(results, key=lambda x: x['row'][-1], reverse=True)

if __name__ == "__main__":
    from pprint import pprint
    pprint(retrieve_fragments("neural acceleration with pcie"))
