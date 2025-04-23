# folder_sorter.py — deep nested scanner + structure-preserving sorter
import os
import shutil
import yaml

ROOT_DIR = r"C:\real_memory_system"
DEST_DIR = os.path.join(ROOT_DIR, "fragments")
LOG_PATH = os.path.join(ROOT_DIR, "logs", "sort_log.txt")

ALLOWED_EXTENSIONS = {".txt", ".yaml", ".yml", ".json", ".md"}
CATEGORY_FOLDERS = [
    "config", "logic", "scripts", "data", "agent", "context", "misc", "error"
]

os.makedirs(DEST_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

log = []

def extract_category(path):
    try:
        with open(path, "r", encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data.get("category", "misc")
    except Exception as e:
        return "error"

count = 0
for root, _, files in os.walk(ROOT_DIR):
    if DEST_DIR in root:
        continue  # Skip destination to avoid infinite loop

    for filename in files:
        src_path = os.path.join(root, filename)
        if not os.path.isfile(src_path):
            continue

        ext = os.path.splitext(filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            continue  # Skip non-text files

        category = extract_category(src_path)

        # Determine relative path to recreate structure inside category folder
        rel_path = os.path.relpath(src_path, ROOT_DIR)
        nested_path = os.path.join(DEST_DIR, category, os.path.dirname(rel_path))
        os.makedirs(nested_path, exist_ok=True)

        dest_path = os.path.join(nested_path, filename)
        shutil.copy2(src_path, dest_path)

        log.append(f"Moved {rel_path} → {os.path.join(category, os.path.dirname(rel_path))}/")
        count += 1

with open(LOG_PATH, "w", encoding='utf-8') as log_file:
    log_file.write(f"Sorted {count} files.\n\n")
    for entry in log:
        log_file.write(entry + "\n")

print(f"✅ Sorted {count} files from '{ROOT_DIR}' into '{DEST_DIR}' (structure preserved)")
print(f"📄 Log saved to: {LOG_PATH}")
