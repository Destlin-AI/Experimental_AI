from core.config_loader import get
"""
LOGICSHREDDER :: token_agent.py
Purpose: Load YAML beliefs, walk symbolic paths, emit updates to cortex
"""

import os
import yaml
import time
import random
import threading
from utils import agent_profiler
# [PROFILER_INJECTED]
threading.Thread(target=agent_profiler.run_profile_loop, daemon=True).start()
from pathlib import Path
from core.cortex_bus import send_message  # Assumes cortex_bus has send_message function

FRAG_DIR = Path("fragments/core")

class TokenAgent:
    def __init__(self, agent_id="token_agent_01"):
        self.agent_id = agent_id
        self.frag_path = FRAG_DIR
        self.fragment_cache = []

    def load_fragments(self):
        files = list(self.frag_path.glob("*.yaml"))
        random.shuffle(files)
        for f in files:
            with open(f, 'r', encoding='utf-8') as file:
                try:
                    frag = yaml.safe_load(file)
                    if frag:
                        self.fragment_cache.append((f, frag))
                except yaml.YAMLError as e:
                    print(f"[{self.agent_id}] YAML error in {f.name}: {e}")

    def walk_fragment(self, path, frag):
        # Walk logic example: shallow claim reassertion and mutation flag
        if 'claim' not in frag:
            return
        walk_log = {
            'fragment': path.name,
            'claim': frag['claim'],
            'tags': frag.get('tags', []),
            'confidence': frag.get('confidence', 0.5),
            'walk_time': time.time()
        }
        # Randomly flag for mutation
        if random.random() < 0.2:
            walk_log['flag_mutation'] = True
        send_message({
            'from': self.agent_id,
            'type': 'walk_log',
            'payload': walk_log,
            'timestamp': int(time.time())
        })

    def run(self):
        self.load_fragments()
        for path, frag in self.fragment_cache:
            self.walk_fragment(path, frag)
            time.sleep(0.1)  # Optional pacing

if __name__ == "__main__":
    agent = TokenAgent()
    agent.run()
# [CONFIG_PATCHED]
