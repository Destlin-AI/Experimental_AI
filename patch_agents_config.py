"""
LOGICSHREDDER :: patch_agents_config.py
Purpose: Inject config_loader usage into all agents and core modules
"""

from pathlib import Path
import shutil

TARGET_DIRS = ["agents", "core"]
BACKUP_DIR = Path("patch_backups")
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_IMPORT = "from core.config_loader import get"
PATCH_TAG = "# [CONFIG_PATCHED]"

patch_targets = {
    "decay = ": "decay = get('tuning.decay_rate', 0.03)",
    "CONFIDENCE_THRESHOLD = ": "CONFIDENCE_THRESHOLD = get('tuning.cold_logic_threshold', 0.3)",
    "mutation_aggression = ": "mutation_aggression = get('tuning.mutation_aggression', 0.7)",
    "curiosity_bias = ": "curiosity_bias = get('tuning.curiosity_bias', 0.4)",
    "contradiction_sensitivity = ": "contradiction_sensitivity = get('tuning.contradiction_sensitivity', 0.8)",
    "if Path(\"core/neuro.lock\").exists()": "if get('brain.lock_respect') and Path(\"core/neuro.lock\").exists()"
}

def patch_file(path):
    try:
        text = path.read_text(encoding='utf-8')
        if PATCH_TAG in text:
            print(f"[patch] Skipped: {path.name} (already patched)")
            return

        backup_path = BACKUP_DIR / path.name
        shutil.copy(path, backup_path)

        if CONFIG_IMPORT not in text:
            text = CONFIG_IMPORT + "\n" + text

        for old, new in patch_targets.items():
            text = text.replace(old, new)

        text += f"\n{PATCH_TAG}\n"
        path.write_text(text, encoding='utf-8')
        print(f"[patch] [OK] Patched: {path.name}")

    except Exception as e:
        print(f"[patch] ERROR Error on {path.name}: {e}")

def main():
    print("INFO Beginning config patch sweep...")
    for dir_name in TARGET_DIRS:
        path = Path(dir_name)
        if not path.exists():
            print(f"[patch] Directory not found: {dir_name}")
            continue

        for file in path.glob("*.py"):
            patch_file(file)
    print("[OK] Patch complete.")

if __name__ == "__main__":
    main()
