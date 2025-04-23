import os
import json
import duckdb
from pathlib import Path
from datetime import datetime

MEMORY_DIR = "C:/real_memory_system"
LOG_FILE = "logs/report_writer_output.jsonl"
CATEGORY = "auto_ingest"
SUBCATEGORY = "writer_feedback"


def insert_fragment(category, fragment):
    db_path = os.path.join(MEMORY_DIR, f"{category}.duckdb")
    if not os.path.exists(db_path):
        print(f"[SKIP] No DB found for category '{category}'")
        return

    conn = duckdb.connect(db_path)
    conn.execute("""
        INSERT INTO fragments (
            id, claim, sub_category, confidence, tags, timestamp, filepath, content
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        fragment["id"],
        fragment["claim"],
        SUBCATEGORY,
        0.95,
        ["feedback", "agent", "auto"],
        fragment["timestamp"],
        None,
        fragment["output"]
    ))
    conn.close()
    print(f"[✓] Ingested fragment {fragment['id']} into [{category}]")


def feedback_to_memory():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            frag = json.loads(line)
            frag["claim"] = frag["task"][:100]
            insert_fragment(CATEGORY, frag)

if __name__ == "__main__":
    feedback_to_memory()
