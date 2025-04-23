from core.config_loader import get
"""
LOGICSHREDDER :: neuro_lock.py
Purpose: Freeze current belief + memory state into a snapshot archive for backup or audit
"""

import os
import tarfile
import time
import threading
from utils import agent_profiler
# [PROFILER_INJECTED]
threading.Thread(target=agent_profiler.run_profile_loop, daemon=True).start()
from pathlib import Path
import shutil

SNAPSHOT_DIR = Path("snapshots")
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

TARGETS = [
    "fragments/core",
    "logs/",
    "core/cortex_memory.db",
    "fragments/archive",
    "fragments/overflow"
]

LOCK_FILE = Path("core/neuro.lock")

def create_snapshot():
    timestamp = int(time.time())
    filename = SNAPSHOT_DIR / f"logicshredder_snapshot_{timestamp}.tar.gz"
    with tarfile.open(filename, "w:gz") as tar:
        for target in TARGETS:
            path = Path(target)
            if path.exists():
                tar.add(str(path), arcname=path.name)
                print(f"[neuro_lock] Added to archive: {path}")
    print(f"[neuro_lock] Snapshot complete -> {filename.name}")
    return filename

def lock_brain():
    with open(LOCK_FILE, 'w', encoding='utf-8') as lock:
        lock.write(str(int(time.time())))
    print("[neuro_lock] LOGICSHREDDER locked — no mutations will be accepted.")

def unlock_brain():
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
        print("[neuro_lock] Brain unlocked — mutation resumed.")

def is_locked():
    return LOCK_FILE.exists()

def toggle_lock():
    if is_locked():
        unlock_brain()
    else:
        lock_brain()

if __name__ == "__main__":
    print("\nLOGICSHREDDER :: SNAPSHOT + FREEZE SYSTEM")
    print("1. Create snapshot")
    print("2. Toggle lock/unlock")
    print("3. Check lock status")
    choice = input("\nSelect an action: ").strip()

    if choice == "1":
        create_snapshot()
    elif choice == "2":
        toggle_lock()
    elif choice == "3":
        if is_locked():
            print("🔒 Brain is currently LOCKED.")
        else:
            print("INFO Brain is currently ACTIVE.")
    else:
        print("Invalid choice.")
# [CONFIG_PATCHED]
