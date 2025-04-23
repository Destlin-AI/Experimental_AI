from core.config_loader import get
"""
LOGICSHREDDER :: cold_logic_mover.py
Purpose: Move stale, low-confidence beliefs from core to cold storage
"""

import os
import time
import yaml
import threading
from utils import agent_profiler
# [PROFILER_INJECTED]
threading.Thread(target=agent_profiler.run_profile_loop, daemon=True).start()
from pathlib import Path
import shutil

FRAG_DIR = Path("fragments/core")
COLD_DIR = Path("fragments/cold")
LOG_PATH = Path("logs/cold_mover.log")
CONFIDENCE_THRESHOLD = get('tuning.cold_logic_threshold', 0.3)0.3
EMOTION_WEIGHT_PENALTY = 0.15

FRAG_DIR.mkdir(parents=True, exist_ok=True)
COLD_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def is_stale(fragment):
    confidence = fragment.get('confidence', 0.5)
    emotion = fragment.get('emotion', {})
    emotion_sum = sum(emotion.values()) if isinstance(emotion, dict) else 0.0
    effective_score = confidence - (emotion_sum * EMOTION_WEIGHT_PENALTY)
    return effective_score < CONFIDENCE_THRESHOLD

def log_cold_move(frag_id, from_path, to_path):
    with open(LOG_PATH, 'a', encoding='utf-8') as log:
        log.write(f"[{int(time.time())}] COLD MOVE: {frag_id} -> {to_path.name}\n")

def move_stale_beliefs():
    files = list(FRAG_DIR.glob("*.yaml"))
    for path in files:
        try:
            with open(path, 'r', encoding='utf-8') as file:
                frag = yaml.safe_load(file)
                if frag and is_stale(frag):
                    target = COLD_DIR / path.name
                    shutil.move(str(path), target)
                    log_cold_move(frag.get('id', path.stem), path, target)
                    print(f"[cold_logic_mover] Archived: {path.name}")
        except Exception as e:
            print(f"[cold_logic_mover] Error on {path.name}: {e}")

if __name__ == "__main__":
    while True:
        move_stale_beliefs()
        time.sleep(10)  # Sweep every 10 seconds
# [CONFIG_PATCHED]
