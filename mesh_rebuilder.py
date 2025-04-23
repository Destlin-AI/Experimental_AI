# mesh_rebuilder.py
# CONFIG Auto-crawls current directory tree to rebuild logic mesh configuration
import os
import yaml
from pathlib import Path

BASE = Path(__file__).parent.resolve()
CONFIG_PATH = BASE / "system_config.yaml"
MOUNT_MAP_PATH = BASE / "mount_map.yaml"
BRAINMAP_PATH = BASE / "brainmap.yaml"

logic_roles = {
    "core": ["token_agent.py", "mutation_engine.py", "dreamwalker.py"],
    "cold": ["cold_logic_mover.py", "archive/", "cold_storage/"],
    "incoming": ["guffifier_v2.py", "belief_ingestor.py"],
    "emotion": ["emotion_daemon.py", "emotion_bank.nosql"],
    "subcon": ["subcon_agent.py", "dream_state_loop.py"],
    "fusion": ["fusion_engine.py", "validator.py"],
    "meta": ["meta_agent.py", "feedback_daemon.py"]
}

def find_role(path):
    for role, keywords in logic_roles.items():
        for keyword in keywords:
            if keyword in str(path):
                return role
    return "unassigned"

def crawl_and_map():
    logic_mounts = {}
    brainmap = {}
    for root, dirs, files in os.walk(BASE):
        for f in files:
            path = Path(root) / f
            role = find_role(path)
            if role not in logic_mounts:
                logic_mounts[role] = []
            logic_mounts[role].append(str(path.relative_to(BASE)))
            brainmap[str(path.relative_to(BASE))] = role
    return logic_mounts, brainmap

def write_yaml(data, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False)

def rebuild_config():
    mounts, brainmap = crawl_and_map()

    system_config = {
        "base_path": str(BASE),
        "logic_zones": list(mounts.keys()),
        "fragment_format": "yaml",
        "storage_mode": "hybrid"
    }

    print(f"🔍 Scanned base: {BASE}")
    print(f"INFO Zones found: {list(mounts.keys())}")
    print(f"💾 Writing: {CONFIG_PATH}, {MOUNT_MAP_PATH}, {BRAINMAP_PATH}")

    write_yaml(system_config, CONFIG_PATH)
    write_yaml(mounts, MOUNT_MAP_PATH)
    write_yaml(brainmap, BRAINMAP_PATH)

    print("[OK] Mesh rebuild complete.")

if __name__ == "__main__":
    rebuild_config()
