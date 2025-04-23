"""
LOGICSHREDDER :: patch_auto_configurator_disks.py
Purpose: Patch auto_configurator.py with multi-disk detection logic
"""

from pathlib import Path
import shutil

TARGET = Path("auto_configurator.py")
BACKUP = Path("auto_configurator.backup.py")

PATCH_FUNC = '''
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
'''

def patch_file():
    if not TARGET.exists():
        print("[patch] ERROR File not found: auto_configurator.py")
        return

    shutil.copy(TARGET, BACKUP)
    print("[patch] 📋 Backup saved as:", BACKUP.name)

    code = TARGET.read_text(encoding='utf-8')
    start = code.find("def get_system_profile()")
    end = code.find("def", start + 10)

    if start == -1:
        print("[patch] ERROR Could not find original function.")
        return

    # Replace old function
    new_code = code[:start] + PATCH_FUNC + "\n" + code[end:]
    TARGET.write_text(new_code, encoding='utf-8')

    print("[patch] [OK] auto_configurator.py successfully patched with multi-disk awareness.")

if __name__ == "__main__":
    patch_file()
