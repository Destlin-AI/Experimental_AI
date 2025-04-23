"""
LOGICSHREDDER :: patch_config_references.py
Purpose: Replace old core.config_loader references with core.config_access
"""

from pathlib import Path
import shutil

BASE_DIR = Path(".")
BACKUP_DIR = Path("patch_backups_config_access")
BACKUP_DIR.mkdir(exist_ok=True)

TARGET = "core.config_loader"
REPLACEMENT = "core.config_access"

def patch_file(path):
    try:
        code = path.read_text(encoding='utf-8')
        if TARGET not in code or REPLACEMENT in code:
            return False

        backup_path = BACKUP_DIR / path.name
        shutil.copy(path, backup_path)

        patched = code.replace(TARGET, REPLACEMENT)
        path.write_text(patched, encoding='utf-8')
        print(f"[patch] [OK] Patched: {path}")
        return True
    except Exception as e:
        print(f"[patch] ERROR Error patching {path}: {e}")
        return False

def main():
    print("[patch] 🔍 Searching for config_loader references...")
    for file in BASE_DIR.rglob("*.py"):
        patch_file(file)
    print("[patch] 🎉 Config access references updated.")

if __name__ == "__main__":
    main()
