import os, shutil, hashlib
from pathlib import Path

# Destination directory
DEST = Path("C:/real_memory_system/models/unified")
DEST.mkdir(parents=True, exist_ok=True)

# Extensions to match
VALID_EXTS = {".gguf", ".bin", ".pt", ".onnx", ".pth"}

# Directories to scan (adjust as needed)
SCAN_DIRS = [
    Path("C:/Users/PC/Desktop/WORKTABLE2"),
    Path("C:/Users/PC/Documents"),
    Path("C:/Users/PC/Downloads"),
    Path("C:/Users/PC/Dropbox"),
    Path("C:/real_memory_system/models"),
]

# Seen hashes to prevent duplicates
seen_hashes = {}

def hash_file(path):
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except:
        return None

def move_model(file_path):
    file_hash = hash_file(file_path)
    if not file_hash:
        print(f"[!] Failed to hash: {file_path}")
        return

    if file_hash in seen_hashes:
        print(f"[⏩] Duplicate skipped: {file_path}")
        return

    seen_hashes[file_hash] = True
    dest_path = DEST / file_path.name
    if not dest_path.exists():
        shutil.copy2(file_path, dest_path)
        print(f"[✅] Moved: {file_path.name}")

def scan_and_move():
    print(f"[🔍] Scanning model locations...")
    for folder in SCAN_DIRS:
        if not folder.exists(): continue
        for root, _, files in os.walk(folder):
            for file in files:
                ext = Path(file).suffix.lower()
                if ext in VALID_EXTS:
                    move_model(Path(root) / file)

if __name__ == "__main__":
    scan_and_move()
    print(f"\n[🏁] Complete. All unique models are in: {DEST}")
