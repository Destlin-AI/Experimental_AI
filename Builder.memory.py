
# === BATCH 1: Builder.memory.py ===

import os
import duckdb
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS fragments (
    id TEXT PRIMARY KEY,
    claim TEXT,
    sub_category TEXT,
    confidence DOUBLE,
    tags TEXT[],
    origin TEXT,
    filepath TEXT,
    timestamp TIMESTAMP,
    content TEXT
);
"""

DEFAULT_CATEGORIES = [
    "logic", "tools", "agents", "plans", "dreams", "errors", "ethics",
    "external", "symbols", "language", "ai_history", "hardware", "runtime_logs",
    "reflections", "inspiration", "coldstore", "boot", "contexts", "beliefs"
]

BASE = Path("D:/Project_AI")
DB_PATH = BASE / "memory_db"
FRAG_PATH = BASE / "fragments"
PRES_PATH = BASE / "preserved"

def init_memory_system(categories=None):
    if categories is None:
        categories = DEFAULT_CATEGORIES

    for cat in categories:
        db_file = DB_PATH / f"{cat}.duckdb"
        db_file.parent.mkdir(parents=True, exist_ok=True)
        conn = duckdb.connect(str(db_file))
        conn.execute(SCHEMA)
        conn.close()

        # Mirror folders
        (FRAG_PATH / cat).mkdir(parents=True, exist_ok=True)
        (PRES_PATH / cat).mkdir(parents=True, exist_ok=True)

    print(f"[✅] Initialized {len(categories)} memory categories.")

if __name__ == "__main__":
    init_memory_system()
