"""
LOGICSHREDDER :: auto_configurator.py
Purpose: Scan system and assign optimal config values based on hardware
"""

import psutil
import yaml
from pathlib import Path
import platform
import time

CONFIG_PATH = Path("configs/system_config.yaml")
BACKUP_PATH = CONFIG_PATH.with_suffix(".autobackup.yaml")


def get_system_profile():
    disks = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            disks.append({
                "mount": part.mountpoint,
                "fstype": part.fstype,
                "free_gb": round(usage.free / (1024**3), 2),
                "total_gb": round(usage.total / (1024**3), 2)
            })
        except PermissionError:
            continue

    total_free = sum(d['free_gb'] for d in disks)
    primary = disks[0] if disks else {"mount": "?", "free_gb": 0}

    return {
        "cores": psutil.cpu_count(logical=False),
        "threads": psutil.cpu_count(logical=True),
        "total_ram": round(psutil.virtual_memory().total / (1024**2)),
        "available_ram": round(psutil.virtual_memory().available / (1024**2)),
        "disks": disks,
        "disk_free_total": round(total_free, 2),
        "disk_primary_mount": primary["mount"],
        "platform": platform.system()
    }

def generate_config(profile):
    cfg = {
        "brain": {
            "name": "LOGICSHREDDER",
            "version": 1.0,
            "allow_mutation": profile["cores"] >= 2,
            "allow_cold_storage": True,
            "auto_snapshot": profile["disk_free_total"] >= 5,
            "emotion_enabled": profile["total_ram"] >= 4000,
            "safe_mode": False,
            "lock_respect": True,
            "optimized_by": "auto_configurator"
        },
        "resources": {
            "cpu_limit_percent": 90 if profile["cores"] >= 4 else 70,
            "min_ram_mb": 2048 if profile["total_ram"] < 4000 else 4096,
            "io_watchdog_enabled": True,
            "max_io_mb_per_minute": 300 if profile["disk_free"] < 2 else 500
        },
        "paths": {
            "fragments": "fragments/core/",
            "archive": "fragments/archive/",
            "overflow": "fragments/overflow/",
            "cold": "fragments/cold/",
            "logs": "logs/",
            "profiler": "logs/agent_stats/",
            "snapshot": "snapshots/",
            "input": "input/"
        },
        "agents": {
            "token_agent": True,
            "guffifier": True,
            "mutation_engine": profile["cores"] >= 2,
            "validator": True,
            "dreamwalker": profile["cores"] >= 4,
            "cold_logic_mover": True,
            "meta_agent": True,
            "cortex_logger": True,
            "heatmap": profile["total_ram"] >= 3000
        },
        "security": {
            "auto_lock_on_snapshot": True,
            "forbid_external_io": True,
            "network_disabled": True,
            "write_protect_brain": False
        },
        "modes": {
            "verbose_logging": True,
            "batch_mode": False,
            "ignore_errors": False,
            "dry_run": False
        },
        "tuning": {
            "contradiction_sensitivity": 0.8,
            "decay_rate": 0.02 if profile["cores"] >= 4 else 0.04,
            "mutation_aggression": 0.7 if profile["cores"] >= 4 else 0.4,
            "rewalk_threshold": 0.6,
            "cold_logic_threshold": 0.3,
            "curiosity_bias": 0.3 if profile["available_ram"] > 3000 else 0.1
        }
    }
    return cfg

def write_config(cfg):
    if CONFIG_PATH.exists():
        CONFIG_PATH.replace(BACKUP_PATH)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as out:
        yaml.dump(cfg, out)
    print(f"[auto_configurator] [OK] Config written to {CONFIG_PATH.name}")
    print(f"[auto_configurator] INFO System optimized by logic profile.")

def main():
    profile = get_system_profile()
    print("[auto_configurator] INFO Detected system profile:")
    for k, v in profile.items():
        print(f"  - {k}: {v}")
    config = generate_config(profile)
    write_config(config)

if __name__ == "__main__":
    main()
