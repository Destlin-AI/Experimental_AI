# === BATCH 5: nvme_fragment_cache.py ===

import os
import duckdb
from pathlib import Path
from datetime import datetime
import shutil

MEMORY_DB = Path("D:/Project_AI/memory_db")
NVME_CACHE = Path("D:/Project_AI/meta/nvme_cache")
NVME_CACHE.mkdir(parents=True, exist_ok=True)

def dump_fragments_to_nvme(threshold=0.9):
    for db_file in MEMORY_DB.glob("*.duckdb"):
        cat = db_file.stem
        try:
            conn = duckdb.connect(str(db_file))
            res = conn.execute(f"""
                SELECT * FROM fragments
                WHERE confidence >= {threshold}
                ORDER BY timestamp DESC
                LIMIT 200
            """).fetchall()
            dest = NVME_CACHE / f"{cat}_nvme_fragments.txt"
            with open(dest, "w", encoding="utf-8") as f:
                for row in res:
                    f.write(f"[{row[2]}] {row[1]}\n")
            print(f"[⚡] {cat}: Cached {len(res)} fragments to NVMe")
            conn.close()
        except Exception as e:
            print(f"[❌] Error caching {cat}: {e}")

if __name__ == "__main__":
    dump_fragments_to_nvme(threshold=0.9)
