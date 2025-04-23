import os
import tarfile
from datetime import datetime

EXPORT_DIR = os.path.expanduser("~/neurostore/backups")
SOURCE_DIRS = ["agents", "fragments", "logs", "meta", "runtime", "data"]

os.makedirs(EXPORT_DIR, exist_ok=True)
backup_name = f"neurostore_brain_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
backup_path = os.path.join(EXPORT_DIR, backup_name)

with tarfile.open(backup_path, "w:gz") as tar:
    for folder in SOURCE_DIRS:
        if os.path.exists(folder):
            print(f"[+] Archiving {folder}/")
            tar.add(folder, arcname=folder)
        else:
            print(f"[-] Skipped missing folder: {folder}")

print(f"[OK] Brain backup complete -> {backup_path}")
