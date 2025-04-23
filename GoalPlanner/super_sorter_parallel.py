# === BATCH 3: super_sorter_parallel.py ===

import os
import uuid
import yaml
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

FRAG_PATH = Path("D:/Project_AI/fragments")
CATEGORIES = [
    "logic", "tools", "agents", "plans", "dreams", "errors", "ethics",
    "external", "symbols", "language", "ai_history", "hardware", "runtime_logs",
    "reflections", "inspiration", "coldstore", "boot", "contexts", "beliefs"
]

def sort_and_store_fragment(text, category, subcat="uncategorized", tags=None, origin="system"):
    fid = str(uuid.uuid4())
    frag = {
        "id": fid,
        "claim": text.strip(),
        "sub_category": subcat,
        "confidence": 1.0,
        "tags": tags or [],
        "origin": origin,
        "filepath": str(FRAG_PATH / category / f"{fid}.yaml"),
        "timestamp": datetime.utcnow().isoformat(),
        "content": text.strip()
    }
    path = FRAG_PATH / category / f"{fid}.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(frag, f)
    print(f"[💾] Stored fragment to: {path.name}")
    return frag

def batch_sort(texts, category="logic"):
    with ThreadPoolExecutor() as pool:
        pool.map(lambda t: sort_and_store_fragment(t, category), texts)

if __name__ == "__main__":
    # Example usage:
    batch_sort([
        "AI should not lie unless under directive.",
        "PCIe 5.0 lanes can be used for side-channel memory hacks.",
        "A fragment may contradict another but not overwrite it."
    ])
