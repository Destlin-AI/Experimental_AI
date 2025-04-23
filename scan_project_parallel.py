# scan_project_parallel.py
import os
import hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

OUTPUT_FILE = "project_inventory.md"
SCAN_DIR = Path.cwd()
EXTS = {".py", ".sh", ".txt", ".md", ".yaml", ".yml", ".json"}

def hash_file(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()[:12]
    except Exception:
        return "unreadable"

def collect_summary(path):
    try:
        lines = path.read_text(errors="ignore").splitlines()
        head = "\n".join(lines[:10])
        return f"🔹 **{path.name}** `{hash_file(path)}`\n### `{path}`\n\n```\n{head}\n```\n"
    except Exception:
        return f"🔹 **{path.name}** `unreadable`\n### `{path}`\n\n(unreadable)\n\n"

def worker(path):
    if path.suffix.lower() in EXTS:
        return collect_summary(path)
    return None

def scan_all_parallel(base_path):
    all_files = [p for p in base_path.rglob("*") if p.is_file()]
    results = []

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(worker, p): p for p in all_files}
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    return results

if __name__ == "__main__":
    print("⚡ Scanning with multicore fan-out...")
    content = "# 🧠 Project Inventory (Parallel Scan)\n\n"
    content += "\n\n".join(scan_all_parallel(SCAN_DIR))
    Path(OUTPUT_FILE).write_text(content, encoding="utf-8")
    print(f"✅ Done. Output saved to {OUTPUT_FILE}")
