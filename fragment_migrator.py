"""
LOGICSHREDDER :: fragment_migrator.py
Purpose: Migrate legacy flat fragments to structured subject-predicate-object format
"""

import yaml
import re
import time
from pathlib import Path

TARGET_DIRS = [
    Path("fragments/core"),
    Path("fragments/incoming")
]

LOG_PATH = Path("logs/migration_log.txt")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def parse_claim(claim_text):
    match = re.match(r"The (\w+) (is|are|was|were|has|have) (.+)", claim_text.strip(), re.IGNORECASE)
    if match:
        return {
            "subject": match.group(1),
            "predicate": match.group(2),
            "object": match.group(3).strip(". ")
        }
    return None

def migrate_fragment(path):
    try:
        frag = yaml.safe_load(path.read_text(encoding='utf-8'))
        if not frag or "claim" not in frag:
            return False  # Already migrated or malformed

        claim = frag.pop("claim")
        struct = parse_claim(claim)

        if not struct:
            print(f"[migrator] ERROR Unable to structure: {claim}")
            return False

        frag["structure"] = struct
        path.write_text(yaml.dump(frag), encoding='utf-8')

        with open(LOG_PATH, 'a', encoding='utf-8') as log:
            log.write(f"[{int(time.time())}] Migrated {path.name} -> structured format\n")

        print(f"[migrator] [OK] Migrated: {path.name}")
        return True

    except Exception as e:
        print(f"[migrator] ERROR Error on {path.name}: {e}")
        return False

def run_migration():
    print("CONFIG Starting fragment migration...")
    for dir_path in TARGET_DIRS:
        if not dir_path.exists():
            continue
        for frag_file in dir_path.glob("*.yaml"):
            migrate_fragment(frag_file)
    print("[OK] Migration complete.")

if __name__ == "__main__":
    run_migration()
