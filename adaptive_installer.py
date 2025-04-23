# adaptive_installer.py
import os
import yaml
import psutil
import platform
from pathlib import Path
from shutil import disk_usage

BASE = Path(__file__).parent
CONFIG_PATH = BASE / "system_config.yaml"

def detect_disks():
    disks = []
    for part in psutil.disk_partitions():
        try:
            usage = disk_usage(part.mountpoint)
            disks.append({
                'mount': part.mountpoint,
                'fstype': part.fstype,
                'free_gb': round(usage.free / 1e9, 2),
                'total_gb': round(usage.total / 1e9, 2)
            })
        except Exception:
            continue
    return disks

def choose_primary_mount(disks):
    if not disks:
        return "C:\\" if platform.system() == "Windows" else "/"
    return disks[0]['mount']

def detect_tier(profile):
    ram = profile['ram_total_mb']
    cores = profile['threads']
    has_nvme = any(d['mount'][0].upper() in ['C', 'D', 'F'] for d in profile['disks'])

    if ram < 8000 or cores < 2:
        return "tier_0_minimal"
    elif ram < 16000:
        return "tier_1_agent"
    elif ram < 64000:
        return "tier_2_blade"
    elif ram >= 64000 and has_nvme:
        return "tier_3_controller"
    else:
        return "tier_unknown"

def generate_config(profile):
    return {
        'platform': profile['os'],
        'cpu_cores': profile['cpu_cores'],
        'threads': profile['threads'],
        'ram_total': profile['ram_total_mb'],
        'ram_available': profile['ram_available_mb'],
        'disk_primary_mount': choose_primary_mount(profile['disks']),
        'disk_free_total': profile['disk_free'],
        'logic_tier': detect_tier(profile),
        'logic_root': 'C:/logicshred/' if profile['os'] == "Windows" else '/neurostore/',
        'logic_ram': {},
        'fragment_defaults': {
            'emotion_decay': True,
            'mutation_rate': 'auto'
        }
    }

def get_profile():
    ram_total = psutil.virtual_memory().total
    ram_available = psutil.virtual_memory().available
    cpu_count = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count()
    disks = detect_disks()
    total_disk_free = sum([d['free_gb'] for d in disks])

    return {
        'os': platform.system(),
        'cpu_cores': cpu_count,
        'threads': cpu_threads,
        'ram_total_mb': round(ram_total / 1e6),
        'ram_available_mb': round(ram_available / 1e6),
        'disks': disks,
        'disk_free': round(total_disk_free, 2)
    }

def write_yaml(config):
    with open(CONFIG_PATH, 'w') as f:
        yaml.safe_dump(config, f)

def main():
    print("[auto_configurator] INFO Detected system profile:")
    profile = get_profile()
    for k, v in profile.items():
        print(f"  - {k}: {v}")
    config = generate_config(profile)
    write_yaml(config)
    print(f"[auto_configurator] [OK] Config written to {CONFIG_PATH.name}")
    print(f"[auto_configurator] INFO System optimized by logic profile: {config['logic_tier']}")

if __name__ == "__main__":
    main()
