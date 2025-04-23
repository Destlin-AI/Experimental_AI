"""
LOGICSHREDDER :: path_optimizer.py
Purpose: Benchmark all mounted drives and assign best paths in config
"""

import psutil
import time
import os
import tempfile
from pathlib import Path
import yaml

CONFIG_PATH = Path("configs/system_config.yaml")
BENCH_FILE = "shredspeed.tmp"

def benchmark_disk(mountpoint, duration=1.5):
    path = Path(mountpoint) / BENCH_FILE
    block = b"x" * 4096
    try:
        # Write test
        start = time.perf_counter()
        with open(path, 'wb') as f:
            while time.perf_counter() - start < duration:
                f.write(block)
        write_time = time.perf_counter() - start

        # Read test
        start = time.perf_counter()
        with open(path, 'rb') as f:
            while f.read(4096):
                pass
        read_time = time.perf_counter() - start

        ops = round((duration / write_time + duration / read_time) / 2, 2)
        path.unlink(missing_ok=True)
        return ops
    except Exception as e:
        print(f"[path_optimizer] ERROR Skipped {mountpoint}: {e}")
        return 0.0

def find_best_disks():
    candidates = []
    for part in psutil.disk_partitions(all=False):
        try:
            if "cdrom" in part.opts.lower() or part.fstype == "":
                continue
            usage = psutil.disk_usage(part.mountpoint)
            speed = benchmark_disk(part.mountpoint)
            candidates.append({
                "mount": part.mountpoint,
                "free_gb": round(usage.free / (1024**3), 2),
                "speed_score": speed
            })
        except:
            continue
    return sorted(candidates, key=lambda x: x["speed_score"], reverse=True)

def write_path_config(disks):
    if not disks:
        print("[path_optimizer] No valid disks found.")
        return

    paths = {
        "fragments": Path(disks[0]["mount"]) / "logicshred/fragments/core/",
        "archive": Path(disks[-1]["mount"]) / "logicshred/fragments/archive/",
        "cold": Path(disks[-1]["mount"]) / "logicshred/fragments/cold/",
        "overflow": Path(disks[-1]["mount"]) / "logicshred/fragments/overflow/",
        "logs": Path(disks[1 if len(disks) > 1 else 0]["mount"]) / "logicshred/logs/",
        "profiler": Path(disks[1 if len(disks) > 1 else 0]["mount"]) / "logicshred/logs/agent_stats/",
        "snapshot": Path(disks[-1]["mount"]) / "logicshred/snapshots/",
        "input": Path(disks[0]["mount"]) / "logicshred/input/"
    }

    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    else:
        config = {}

    config['paths'] = {k: str(v).replace("\\", "/") for k, v in paths.items()}
    config['brain']['optimized_by'] = "path_optimizer"

    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        yaml.dump(config, f)

    print("[path_optimizer] [OK] Config paths updated for optimal storage.")

def main():
    print("[path_optimizer] LAUNCH Scanning all drives...")
    disks = find_best_disks()
    for d in disks:
        print(f"  {d['mount']} -> {d['speed_score']} ops/sec | Free: {d['free_gb']} GB")
    write_path_config(disks)

if __name__ == "__main__":
    main()
