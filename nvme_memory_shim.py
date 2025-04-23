import os
import time
import yaml
import psutil
from pathlib import Path
from shutil import disk_usage

BASE = Path(__file__).parent
CONFIG_PATH = BASE / "system_config.yaml"
LOGIC_CACHE = BASE / "hotcache"

def detect_nvmes():
    nvmes = []
    fallback_mounts = ['C', 'D', 'E', 'F']
    for part in psutil.disk_partitions():
        label = part.device.lower()
        try:
            usage = disk_usage(part.mountpoint)
            is_nvme = any(x in label for x in ['nvme', 'ssd'])
            is_fallback = part.mountpoint.strip(':').upper() in fallback_mounts
            if is_nvme or is_fallback:
                nvmes.append({
                    'mount': part.mountpoint,
                    'fstype': part.fstype,
                    'free_gb': round(usage.free / 1e9, 2),
                    'total_gb': round(usage.total / 1e9, 2)
                })
        except Exception:
            continue
    print(f"[shim] Detected {len(nvmes)} logic-capable drive(s): {[n['mount'] for n in nvmes]}")
    return sorted(nvmes, key=lambda d: d['free_gb'], reverse=True)

def assign_as_logic_ram(nvmes):
    logic_zones = {}
    for i, nvme in enumerate(nvmes[:4]):
        zone = f"ram_shard_{i+1}"
        path = Path(nvme['mount']) / "logicshred_cache"
        path.mkdir(exist_ok=True)
        logic_zones[zone] = str(path)
    return logic_zones

def update_config(zones):
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {}
    config['logic_ram'] = zones
    config['hotcache_path'] = str(LOGIC_CACHE)
    with open(CONFIG_PATH, 'w') as f:
        yaml.safe_dump(config, f)
    print(f"[OK] Config updated with NVMe logic cache: {list(zones.values())}")

if __name__ == "__main__":
    LOGIC_CACHE.mkdir(exist_ok=True)
    print("[INFO] Detecting NVMe drives and logic RAM mounts...")
    drives = detect_nvmes()
    if not drives:
        print("[WARN] No NVMe or fallback drives detected. System unchanged.")
    else:
        zones = assign_as_logic_ram(drives)
        update_config(zones)
