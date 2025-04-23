# logic_ram_scheduler.py
import os
import yaml
import psutil
import time
import threading
import subprocess
from pathlib import Path
from shutil import copyfile

BASE = Path(__file__).parent
CONFIG_PATH = BASE / "system_config.yaml"
ADAPTIVE_INSTALLER = BASE / "adaptive_installer.py"
FRAG_ROOT = BASE / "fragments" / "core"

def ensure_config_exists():
    if not CONFIG_PATH.exists():
        print("INFO system_config.yaml not found. Running adaptive_installer.py...")
        result = subprocess.run(["python", str(ADAPTIVE_INSTALLER)], capture_output=True, text=True)
        if result.returncode != 0:
            print("ERROR Failed to run adaptive_installer.py:")
            print(result.stderr)
            exit(1)
        print("[OK] system_config.yaml generated.")

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def get_ram_shards(config):
    return config.get("logic_ram", {})

def list_fragments(source):
    return list(Path(source).glob("*.yaml"))

def schedule_fragments_to_cache(fragments, shard_paths, per_shard=20):
    shards = list(shard_paths.values())
    if not shards:
        print("ERROR No logic shards found in config.")
        return

    total = len(fragments)
    assigned = 0

    for i, frag in enumerate(fragments):
        target_shard = Path(shards[i % len(shards)])
        dest = target_shard / frag.name
        try:
            copyfile(frag, dest)
            assigned += 1
        except Exception as e:
            print(f"[scheduler] Failed to assign {frag.name}: {e}")

    print(f"[OK] Assigned {assigned}/{total} fragments to {len(shards)} shard(s).")

def preload_scheduler():
    ensure_config_exists()
    config = load_config()
    shards = get_ram_shards(config)

    if not shards:
        print("WARNING No logic RAM shards defined.")
        return

    print("📦 Scanning logic fragments...")
    fragments = list_fragments(FRAG_ROOT)
    if not fragments:
        print("WARNING No fragments found in core/")
        return

    schedule_fragments_to_cache(fragments, shards)

def monitor_and_reload(interval=60):
    while True:
        preload_scheduler()
        time.sleep(interval)

if __name__ == "__main__":
    thread = threading.Thread(target=monitor_and_reload, daemon=True)
    thread.start()
    print("INFO logic_ram_scheduler running in background. CTRL+C to kill.")
    while True:
        time.sleep(9999)
