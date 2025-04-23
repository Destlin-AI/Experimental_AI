"""
LOGICSHREDDER :: fragment_teleporter.py
Purpose: Move fragments to their optimized locations as defined in system_config.yaml
"""

import os
import shutil
import yaml
from pathlib import Path
from core.config_loader import load_config

def get_paths():
    config = load_config()
    if "paths" not in config:
        print("[teleporter] ERROR Config missing 'paths'.")
        return None

    return {k: Path(v) for k, v in config["paths"].items()}

def move_all(source_dir, dest_dir):
    count = 0
    if not source_dir.exists():
        return 0

    dest_dir.mkdir(parents=True, exist_ok=True)
    for file in source_dir.glob("*.yaml"):
        try:
            shutil.move(str(file), str(dest_dir / file.name))
            count += 1
        except Exception as e:
            print(f"[teleporter] WARNING Failed to move {file.name}: {e}")
    return count

def run_teleport():
    print("[teleporter] 🚚 Starting logic fragment migration...")
    paths = get_paths()
    if not paths:
        return

    old_dirs = [
        Path("fragments/core"),
        Path("fragments/incoming"),
        Path("fragments/cold"),
        Path("fragments/archive"),
        Path("fragments/overflow")
    ]

    teleport_map = {
        "fragments/core": paths["fragments"],
        "fragments/incoming": paths["fragments"],
        "fragments/cold": paths["cold"],
        "fragments/archive": paths["archive"],
        "fragments/overflow": paths["overflow"]
    }

    total = 0
    for old_dir in old_dirs:
        target = teleport_map.get(str(old_dir).replace("\\", "/"), None)
        if target:
            moved = move_all(old_dir, target)
            total += moved
            print(f"[teleporter] [OK] Moved {moved} from {old_dir.name} -> {target}")
        else:
            print(f"[teleporter] WARNING No target mapped for: {old_dir.name}")

    print(f"[teleporter] ✨ Total fragments relocated: {total}")

if __name__ == "__main__":
    run_teleport()
