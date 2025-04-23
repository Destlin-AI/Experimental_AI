"""
LOGICSHREDDER :: deep_system_scan.py
Purpose: Perform full hardware + performance scan for AI self-awareness
"""

import platform
import psutil
import shutil
import os
from pathlib import Path
import json

REPORT_PATH = Path("logs/hardware_profile.json")
REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

def detect_gpu():
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        return [{
            "name": gpu.name,
            "driver": gpu.driver,
            "memory_total_MB": gpu.memoryTotal,
            "uuid": gpu.uuid
        } for gpu in gpus]
    except:
        return []

def get_drive_types():
    result = []
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
            result.append({
                "mount": part.mountpoint,
                "fstype": part.fstype,
                "free_gb": round(usage.free / (1024**3), 2),
                "total_gb": round(usage.total / (1024**3), 2),
                "device": part.device
            })
        except Exception:
            continue
    return result

def get_cpu_info():
    return {
        "name": platform.processor(),
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "arch": platform.machine(),
        "flags": platform.uname().processor,
    }

def get_memory_info():
    ram = psutil.virtual_memory()
    return {
        "total_MB": round(ram.total / (1024**2)),
        "available_MB": round(ram.available / (1024**2)),
    }

def detect_removables():
    return [
        {
            "mount": part.mountpoint,
            "type": "USB/Removable",
            "fstype": part.fstype
        }
        for part in psutil.disk_partitions(all=False)
        if 'removable' in part.opts.lower()
    ]

def detect_temp():
    temp = Path(os.getenv('TEMP') or "/tmp")
    try:
        usage = shutil.disk_usage(temp)
        return {
            "temp_path": str(temp),
            "free_gb": round(usage.free / (1024**3), 2)
        }
    except:
        return {"temp_path": str(temp), "free_gb": "?"}

def detect_compression_support():
    # Simulate check for known compression-accelerating instructions
    cpu_flags = platform.uname().processor.lower()
    return {
        "zstd_supported": any(k in cpu_flags for k in ["avx2", "avx512", "sse4"]),
        "lz4_optimized": "sse" in cpu_flags,
        "hardware_hint": "possible accelerated zstd/lz4"
    }

def main():
    report = {
        "cpu": get_cpu_info(),
        "ram": get_memory_info(),
        "drives": get_drive_types(),
        "gpu": detect_gpu(),
        "removable": detect_removables(),
        "temp": detect_temp(),
        "compression_support": detect_compression_support()
    }

    with open(REPORT_PATH, 'w', encoding='utf-8') as out:
        json.dump(report, out, indent=2)

    print(f"[OK] Hardware profile saved to {REPORT_PATH}")

if __name__ == "__main__":
    main()
