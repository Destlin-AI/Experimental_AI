import yaml, time, shutil
from pathlib import Path

INDEX = Path("meta/memory_index.yaml")
CORE = Path("fragments/core")
ARCHIVE = Path("fragments/archive")
AGE_LIMIT = 86400 * 3  # 3 days

def load_index():
    with open(INDEX, 'r') as f:
        return yaml.safe_load(f)

def archive_logic():
    now = int(time.time())
    index = load_index()
    changes = 0

    for fid, meta in index.items():
        last_seen = meta.get('last_seen', now)
        if now - last_seen > AGE_LIMIT and meta.get('status') == 'active':
            fpath = CORE / f"{fid}.yaml"
            if fpath.exists():
                shutil.move(str(fpath), ARCHIVE / f"{fid}.yaml")
                meta['status'] = 'archived'
                changes += 1

    with open(INDEX, 'w') as f:
        yaml.dump(index, f)
    print(f"[memory_archiver] Archived: {changes}")

if __name__ == "__main__":
    archive_logic()
