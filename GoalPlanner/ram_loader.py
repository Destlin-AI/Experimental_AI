# === BATCH 4: ram_loader.py ===

import os
import duckdb
import shutil
from pathlib import Path

MEMORY_DB = Path("D:/Project_AI/memory_db")
RAM_CACHE = Path("D:/Project_AI/meta/hotcache")

CATEGORIES = [f.stem for f in MEMORY_DB.glob("*.duckdb")]
RAM_CACHE.mkdir(parents=True, exist_ok=True)

def preload_to_ram(top_n=100):
    for cat in CATEGORIES:
        db_path = MEMORY_DB / f"{cat}.duckdb"
        if not db_path.exists():
            continue
        try:
            conn = duckdb.connect(str(db_path))
            result = conn.execute(f"""
                SELECT * FROM fragments
                ORDER BY confidence DESC
                LIMIT {top_n}
            """).fetchall()
            cache_file = RAM_CACHE / f"{cat}_cache.txt"
            with open(cache_file, "w", encoding="utf-8") as f:
                for row in result:
                    f.write(f"[{row[2]}] {row[1]}\n")
            print(f"[🧠] Cached {len(result)} fragments from '{cat}'")
            conn.close()
        except Exception as e:
            print(f"[⚠️] RAM load failed on {cat}: {e}")

if __name__ == "__main__":
    preload_to_ram(top_n=100)
