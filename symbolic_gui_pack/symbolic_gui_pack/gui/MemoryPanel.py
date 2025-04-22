import os
import duckdb
from pathlib import Path

MEMORY_DB = Path("C:/real_memory_system/memory_db/master.duckdb")

def list_fragment_summary():
    if not MEMORY_DB.exists():
        return {"error": "Memory database not found."}

    conn = duckdb.connect(str(MEMORY_DB))
    try:
        result = conn.execute(
            """
            SELECT sub_category, COUNT(*) as count
            FROM fragments
            GROUP BY sub_category
            ORDER BY count DESC
            LIMIT 20
            """
        ).fetchall()
    except Exception as e:
        return {"error": str(e)}

    conn.close()
    return [{"category": row[0], "count": row[1]} for row in result]

if __name__ == "__main__":
    summary = list_fragment_summary()
    print(summary)
