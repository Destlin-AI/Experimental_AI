import os
import hashlib
from pathlib import Path
from datetime import datetime
import shutil
import duckdb
from concurrent.futures import ThreadPoolExecutor, as_completed

FEED_DIR = Path("C:/real_memory_system/FEEDING_TIME")
FRAG_DIR = Path("C:/real_memory_system/fragments")
PRESERVE_DIR = Path("C:/real_memory_system/preserved")
LOG_PATH = Path("C:/real_memory_system/logs/sorting.log")
HASH_TRACKER = FRAG_DIR / "hashes"
CHUNK_SIZE = 5120
DB_PATH = Path("C:/real_memory_system/memory.duckdb")

CATEGORY_MAP = {
    ".py": ("code", "python"), ".yaml": ("config", "yaml"), ".yml": ("config", "yaml"),
    ".log": ("logs", "raw"), ".txt": ("notes", "text"), ".md": ("notes", "markdown"),
    ".json": ("data", "json"), ".html": ("web", "html"), ".csv": ("data", "csv"),
    ".duckdb": ("data", "duckdb"), ".db": ("data", "sqlite"),
    ".jpg": ("media", "images"), ".jpeg": ("media", "images"), ".png": ("media", "images"),
    ".webp": ("media", "images"), ".gif": ("media", "images"),
    ".mp4": ("media", "video"), ".mov": ("media", "video"),
    ".avi": ("media", "video"), ".mkv": ("media", "video"),
    ".exe": ("bin", "executables"), ".bin": ("bin", "binaries"),
    ".zip": ("bin", "archives"), ".tar": ("bin", "archives"), ".7z": ("bin", "archives")
}

def log(msg):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] {msg}\n")
    print(f"[SORTER] {msg}")

def hash_file(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def get_category_and_sub(path):
    return CATEGORY_MAP.get(path.suffix.lower(), ("misc", "unknown"))

def insert_into_db(fragment_id, claim, sub_category, tags, timestamp, filepath, content):
    conn = duckdb.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS fragments (
            id TEXT PRIMARY KEY,
            claim TEXT,
            sub_category TEXT,
            confidence DOUBLE,
            tags TEXT[],
            timestamp TIMESTAMP,
            filepath TEXT,
            content TEXT
        )
    """)
    conn.execute("""
        INSERT INTO fragments (
            id, claim, sub_category, confidence, tags, timestamp, filepath, content
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (fragment_id, claim, sub_category, 1.0, tags, timestamp, filepath, content))
    conn.close()

def write_chunk_file(chunk, cat, sub, base, i, source_path):
    chunk_hash = hashlib.sha1(chunk.encode("utf-8")).hexdigest()
    fname = f"{base}_part{i+1}_{chunk_hash[:8]}.txt"
    out_dir = FRAG_DIR / cat / sub
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / fname

    if out_path.exists():
        log(f"Duplicate chunk skipped: {fname}")
        return

    with open(out_path, "w", encoding="utf-8") as out:
        out.write(chunk)

    tags = [cat, sub]
    ts = datetime.now().isoformat()
    insert_into_db(chunk_hash[:12], chunk[:80].strip(), sub, tags, ts, str(out_path), chunk)
    log(f"[OK] Wrote + Indexed: {out_path.name} → {cat}/{sub}")

def preserve_file(path, cat, sub):
    target = PRESERVE_DIR / cat / sub / path.name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)

    ts = datetime.now().isoformat()
    insert_into_db(
        hash_file(path)[:12],
        f"{path.name}",
        sub,
        [cat, sub],
        ts,
        str(target),
        None
    )
    log(f"[PRESERVED] {path.name} → {cat}/{sub}")

def split_and_store(path):
    try:
        cat, sub = get_category_and_sub(path)
        if cat in ["media", "bin", "data"] and path.suffix.lower() not in [".json", ".csv", ".yaml", ".yml"]:
            preserve_file(path, cat, sub)
        else:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if len(content.strip()) < 5:
                log(f"[SKIP] Empty or junk file: {path.name}")
                return

            base = path.stem
            chunks = [content[i:i + CHUNK_SIZE] for i in range(0, len(content), CHUNK_SIZE)]
            for i, chunk in enumerate(chunks):
                write_chunk_file(chunk, cat, sub, base, i, path)

        path.unlink()
        log(f"[🧹] Removed processed file: {path.name}")
    except Exception as e:
        log(f"[ERROR] Failed to process {path.name}: {e}")

def run_super_sorter():
    HASH_TRACKER.mkdir(parents=True, exist_ok=True)
    all_files = []

    for f in FEED_DIR.rglob("*.*"):
        if f.is_file():
            file_hash = hash_file(f)
            hash_record = HASH_TRACKER / f"{file_hash}.ok"
            if not hash_record.exists():
                all_files.append((f, hash_record))

    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = {executor.submit(split_and_store, f[0]): f[1] for f in all_files}
        for future in as_completed(futures):
            try:
                futures[future].touch()
            except Exception as e:
                log(f"[ERROR] Failed to touch hash record: {e}")

if __name__ == "__main__":
    run_super_sorter()
