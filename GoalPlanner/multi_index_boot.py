
import os
import duckdb
from pathlib import Path
from datetime import datetime

DB_PATH = Path("C:/real_memory_system/memory_db")
DB_PATH.mkdir(parents=True, exist_ok=True)

# Scan all category folders
def get_fragment_files(root_folder):
    for dirpath, _, filenames in os.walk(root_folder):
        for f in filenames:
            if f.endswith(".yaml"):
                yield Path(dirpath) / f

def insert_into_db(file_path, conn):
    import yaml
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if not data:
        print(f"[⚠️] Empty: {file_path.name}")
        return

    if isinstance(data, dict):
        data = [data]

    for frag in data:
        conn.execute("""
            INSERT INTO fragments (id, sub_category, claim, confidence, tags, origin, filepath, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            frag.get("id", str(file_path.stem)),
            frag.get("sub_category", "uncategorized"),
            frag.get("claim", ""),
            frag.get("confidence", 1.0),
            frag.get("tags", []),
            frag.get("origin", "unknown"),
            str(file_path),
            datetime.utcnow()
        ))

if __name__ == "__main__":
    print("[🔁] Indexing fragments to DuckDB...")
    db_file = DB_PATH / "master.duckdb"
    conn = duckdb.connect(str(db_file))

    conn.execute("""
        CREATE TABLE IF NOT EXISTS fragments (
            id TEXT PRIMARY KEY,
            sub_category TEXT,
            claim TEXT,
            confidence DOUBLE,
            tags TEXT[],
            origin TEXT,
            filepath TEXT,
            timestamp TIMESTAMP
        )
    """)

    FRAG_PATH = Path("C:/real_memory_system/fragments/")
    for file in get_fragment_files(FRAG_PATH):
        insert_into_db(file, conn)

    print("[✅] Indexing complete.")
    conn.close()
