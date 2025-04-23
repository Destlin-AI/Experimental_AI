"""
LOGICSHREDDER :: memory_tracker.py
Purpose: Track which logic fragments are accessed, reused, or aged
"""

import yaml
import time
from pathlib import Path

FRAG_DIR = Path("fragments/core")
MEMORY_INDEX = Path("logs/memory_index.yaml")
MEMORY_INDEX.parent.mkdir(parents=True, exist_ok=True)

# Load or create memory index
def load_memory():
    if MEMORY_INDEX.exists():
        with open(MEMORY_INDEX, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    return {}

def save_memory(index):
    with open(MEMORY_INDEX, 'w', encoding='utf-8') as f:
        yaml.safe_dump(index, f)

def touch_fragment(frag_id):
    memory = load_memory()
    now = int(time.time())

    if frag_id not in memory:
        memory[frag_id] = {
            "recall_count": 1,
            "last_used": now,
            "first_seen": now,
            "frozen": False,
            "archive_candidate": False
        }
    else:
        memory[frag_id]["recall_count"] += 1
        memory[frag_id]["last_used"] = now

    save_memory(memory)

def log_bulk_fragments(fragment_list):
    memory = load_memory()
    now = int(time.time())
    updated = 0

    for frag in fragment_list:
        frag_id = frag.get("id")
        if not frag_id:
            continue

        if frag_id not in memory:
            memory[frag_id] = {
                "recall_count": 1,
                "last_used": now,
                "first_seen": now,
                "frozen": False,
                "archive_candidate": False
            }
        else:
            memory[frag_id]["recall_count"] += 1
            memory[frag_id]["last_used"] = now

        updated += 1

    save_memory(memory)
    return updated

def forget_old(threshold_days=60):
    memory = load_memory()
    now = int(time.time())
    cutoff = now - (threshold_days * 86400)
    purged = 0

    for frag_id, meta in memory.items():
        if not meta.get("frozen") and meta.get("last_used", 0) < cutoff:
            meta["archive_candidate"] = True
            purged += 1

    save_memory(memory)
    return purged

if __name__ == "__main__":
    print("INFO Tracking current memory usage...")
    updated = forget_old()
    print(f"💾 Marked {updated} fragments as archive candidates.")
