# mount_binder.py
# 🔗 Rebinds orphan .py modules into correct logic zones in mount_map.yaml and brainmap.yaml

import yaml
from pathlib import Path

BASE = Path(__file__).parent
MAP_PATH = BASE / "mount_map.yaml"
BRAIN_PATH = BASE / "brainmap.yaml"
PY_FILES = list(BASE.glob("*.py"))

# Heuristic keyword map
zone_keywords = {
    "core": ["run_logicshredder", "cortex_bus", "dreamwalker"],
    "incoming": ["guffifier", "belief_ingestor"],
    "fusion": ["fusion", "mutation", "validator", "abstraction"],
    "emotion": ["emotion", "fan", "feedback", "heatmap"],
    "meta": ["meta_agent", "boot_wrapper", "auto_configurator"],
    "utils": ["config_loader", "patch", "builder", "optimizer"],
    "cold": ["cold", "archive", "teleporter"],
    "subcon": ["subcon", "dream_state", "sleep", "inner"],
    "quant": ["quant", "prompt", "devourer"],
    "distributed": ["remote", "net", "swarm", "dispatch"]
}

def guess_zone(name):
    for zone, keywords in zone_keywords.items():
        for word in keywords:
            if word.lower() in name.lower():
                return zone
    return "unassigned"

def update_map(path: Path, content: dict):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(content, f, sort_keys=False)

def main():
    print("🔎 Scanning for unbound logic modules...")
    mount_map = {}
    brain_map = {}

    for py in PY_FILES:
        rel_path = str(py.relative_to(BASE))
        zone = guess_zone(py.name)

        if zone not in mount_map:
            mount_map[zone] = []
        mount_map[zone].append(rel_path)
        brain_map[rel_path] = zone

        print(f"[bind] {rel_path} -> {zone}")

    update_map(MAP_PATH, mount_map)
    update_map(BRAIN_PATH, brain_map)
    print(f"[OK] Updated {MAP_PATH.name} + {BRAIN_PATH.name}")

if __name__ == "__main__":
    main()
