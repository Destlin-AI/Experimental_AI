from core.config_loader import get
"""
LOGICSHREDDER :: dreamwalker.py
Purpose: Recursively walk symbolic fragments for deep inference and structural patterns
"""

import os
import yaml
import redis
r = redis.Redis(decode_responses=True)

import time
import random
import threading
from utils import agent_profiler
# [PROFILER_INJECTED]
threading.Thread(target=agent_profiler.run_profile_loop, daemon=True).start()
from pathlib import Path
from core.cortex_bus import send_message

FRAG_DIR = Path("fragments/core")
LOG_PATH = Path("logs/dreamwalker_log.txt")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
FRAG_DIR.mkdir(parents=True, exist_ok=True)

class Dreamwalker:
    def __init__(self, agent_id="dreamwalker_01"):
        self.agent_id = agent_id
        self.visited = set()

    def load_fragment(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            try:
                return yaml.safe_load(file)
            except yaml.YAMLError as e:
                print(f"[{self.agent_id}] YAML error: {e}")
        return None

    def recursive_walk(self, frag, depth=0, lineage=None):
        if not frag or 'claim' not in frag:
            return

        lineage = lineage or []
        lineage.append(frag['claim'])
        frag_id = frag.get('id', str(random.randint(1000, 9999)))
        if frag_id in self.visited or depth > 10:
            return

        self.visited.add(frag_id)

        # Emit walk insight to cortex
if frag.get('confidence', 1.0) < 0.4 and depth > 5:
    r.publish("symbolic_alert", frag['claim'])  # [AUTO_EMIT]
        send_message({
            'from': self.agent_id,
            'type': 'deep_walk_event',
            'payload': {
                'claim': frag['claim'],
                'depth': depth,
                'lineage': lineage[-3:],
                'timestamp': int(time.time())
            },
            'timestamp': int(time.time())
        })

        # Log locally
        with open(LOG_PATH, 'a', encoding='utf-8') as log:
            log.write(f"Depth {depth} :: {' -> '.join(lineage[-3:])}\n")

        # Branch to possible linked fragments (naive reference search)
        links = frag.get('tags', [])
        for file in FRAG_DIR.glob("*.yaml"):
            next_frag = self.load_fragment(file)
            if not next_frag or next_frag.get('id') in self.visited:
                continue
            if any(tag in next_frag.get('tags', []) for tag in links):
                self.recursive_walk(next_frag, depth + 1, lineage[:])

    def run(self):
        frag_files = list(FRAG_DIR.glob("*.yaml"))
        random.shuffle(frag_files)
        for path in frag_files:
            frag = self.load_fragment(path)
            if frag:
                self.recursive_walk(frag)
            time.sleep(0.1)

if __name__ == "__main__":
    Dreamwalker().run()
# [CONFIG_PATCHED]