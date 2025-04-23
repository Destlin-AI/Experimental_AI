from core.config_loader import get
meta_agent.py"""
LOGICSHREDDER :: meta_agent.py
Purpose: Monitor belief activity, curiosity score, mutation depth, and logic heatmap
"""

import yaml
import time
import threading
from utils import agent_profiler
# [PROFILER_INJECTED]
threading.Thread(target=agent_profiler.run_profile_loop, daemon=True).start()
from pathlib import Path
from collections import defaultdict
from core.cortex_bus import send_message

FRAG_DIR = Path("fragments/core")
LOG_PATH = Path("logs/meta_agent.log")
ACTIVITY_TRACKER = Path("logs/walk_activity.log")
MUTATION_LOG = Path("logs/mutation_log.txt")

CURIOUS_THRESHOLD = 30  # Seconds since last walk
HOT_THRESHOLD = 5       # High walk count = recent hotness

def load_walk_activity():
    activity = {}
    if ACTIVITY_TRACKER.exists():
        with open(ACTIVITY_TRACKER, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    timestamp, frag_id = line.strip().split(',')
                    activity[frag_id] = int(timestamp)
                except:
                    continue
    return activity

def load_mutation_counts():
    mutations = defaultdict(int)
    if MUTATION_LOG.exists():
        with open(MUTATION_LOG, 'r', encoding='utf-8') as file:
            for line in file:
                if "Mutation" in line and "from" in line:
                    parts = line.split()
                    new_id = parts[2]
                    parent_id = parts[-1]
                    mutations[parent_id] += 1
    return mutations

def evaluate_fragment(frag_id, last_walk_time, mutation_count):
    now = int(time.time())
    seconds_since_walk = now - last_walk_time
    curiosity_score = min(1.0, seconds_since_walk / 60.0)  # max out at 1.0
    mutation_penalty = min(0.5, mutation_count * 0.05)
    score = curiosity_score - mutation_penalty
    return max(0.0, round(score, 3))

def log_meta(frag_id, score):
    with open(LOG_PATH, 'a', encoding='utf-8') as log:
        log.write(f"[{int(time.time())}] {frag_id}: curiosity={score}\n")

def analyze_fragments():
    activity = load_walk_activity()
    mutations = load_mutation_counts()
    ranked = []

    for path in FRAG_DIR.glob("*.yaml"):
        try:
            frag = yaml.safe_load(path.read_text(encoding='utf-8'))
            frag_id = frag.get('id', path.stem)
            last_walk = activity.get(frag_id, 0)
            mut_count = mutations.get(frag_id, 0)
            score = evaluate_fragment(frag_id, last_walk, mut_count)
            log_meta(frag_id, score)
            if score >= 0.7:
                ranked.append((score, frag_id))
        except Exception as e:
            print(f"[meta_agent] Error analyzing {path.name}: {e}")

    # Emit top curious fragments
    top = sorted(ranked, reverse=True)[:5]
    for score, fid in top:
        send_message({
            'from': 'meta_agent',
            'type': 'curiosity_alert',
            'payload': {'frag_id': fid, 'curiosity': score},
            'timestamp': int(time.time())
        })
        print(f"[meta_agent] CURIOUS: {fid} -> {score}")

if __name__ == "__main__":
    while True:
        analyze_fragments()
        time.sleep(30)  # Every 30s, reassess curiosity
# [CONFIG_PATCHED]
