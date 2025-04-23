from core.config_loader import get
"""
LOGICSHREDDER :: fragment_tools.py
Purpose: Compare symbolic YAML fragments, log diffs, and track mutation drift
"""

import yaml
import difflib
import threading
from utils import agent_profiler
# [PROFILER_INJECTED]
threading.Thread(target=agent_profiler.run_profile_loop, daemon=True).start()
from pathlib import Path
import time

FRAG_DIR = Path("fragments/core")
ARCHIVE_DIR = Path("fragments/archive")
LOG_PATH = Path("logs/fragment_diffs.txt")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def load_fragment(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"[fragment_tools] Failed to load {path}: {e}")
        return None

def compare_fragments(frag1, frag2):
    diffs = {}
    
    if frag1.get('claim') != frag2.get('claim'):
        diffs['claim'] = (frag1.get('claim'), frag2.get('claim'))

    if frag1.get('confidence') != frag2.get('confidence'):
        diffs['confidence'] = (frag1.get('confidence'), frag2.get('confidence'))

    if frag1.get('emotion') != frag2.get('emotion'):
        diffs['emotion'] = (frag1.get('emotion'), frag2.get('emotion'))

    return diffs

def log_diff(old_id, new_id, diffs):
    timestamp = int(time.time())
    with open(LOG_PATH, 'a', encoding='utf-8') as log:
        log.write(f"\n[{timestamp}] Mutation: {old_id} -> {new_id}\n")
        for field, change in diffs.items():
            before, after = change
            log.write(f"  {field}:\n")
            if isinstance(before, str) and isinstance(after, str):
                for line in difflib.unified_diff(
                    before.splitlines(), after.splitlines(),
                    fromfile='before', tofile='after', lineterm=''
                ):
                    log.write(f"    {line}\n")
            else:
                log.write(f"    before: {before}\n")
                log.write(f"    after : {after}\n")

def diff_pair(file1, file2):
    frag1 = load_fragment(file1)
    frag2 = load_fragment(file2)
    if not frag1 or not frag2:
        print("[fragment_tools] Could not load both fragments.")
        return

    diffs = compare_fragments(frag1, frag2)
    if diffs:
        log_diff(frag1.get('id', 'unknown'), frag2.get('id', 'unknown'), diffs)
        print(f"[fragment_tools] Diff recorded for: {frag1.get('id')} -> {frag2.get('id')}")
    else:
        print("[fragment_tools] No significant changes detected.")

if __name__ == "__main__":
    # Manual test mode
    files = list(FRAG_DIR.glob("*.yaml"))
    if len(files) >= 2:
        diff_pair(files[0], files[1])
    else:
        print("[fragment_tools] Not enough fragments to compare.")
# [CONFIG_PATCHED]
