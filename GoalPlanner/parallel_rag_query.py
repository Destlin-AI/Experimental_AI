# === BATCH 6: parallel_rag_query.py ===

import os
import duckdb
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

MEMORY_DB = Path("D:/Project_AI/memory_db")

def search_single_db(db_path, query, confidence_threshold):
    try:
        conn = duckdb.connect(str(db_path))
        results = conn.execute(f"""
            SELECT *, SIMILARITY('{query}', claim) AS sim
            FROM fragments
            WHERE confidence >= {confidence_threshold}
            ORDER BY sim DESC
            LIMIT 10;
        """).fetchall()
        conn.close()
        return [(db_path.stem, r) for r in results]
    except Exception as e:
        print(f"[❌] Failed to search {db_path.name}: {e}")
        return []

def parallel_rag_query(query, confidence_threshold=0.5):
    db_files = list(MEMORY_DB.glob("*.duckdb"))
    all_results = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(search_single_db, db, query, confidence_threshold) for db in db_files]
        for future in futures:
            all_results.extend(future.result())

    return sorted(all_results, key=lambda x: x[1][-1], reverse=True)

if __name__ == "__main__":
    from pprint import pprint
    pprint(parallel_rag_query("pcie memory inference optimizations"))
