"""
LOGICSHREDDER :: mutation_engine.py
Purpose: Apply confidence decay, mutate symbolic beliefs, log ancestry and emit changes
"""

import os
import yaml
import time
import uuid
import random
import redis
from pathlib import Path
from core.cortex_bus import send_message
from utils import agent_profiler
import threading

# Start background profiler
threading.Thread(target=agent_profiler.run_profile_loop, daemon=True).start()

r = redis.Redis(decode_responses=True)

FRAG_DIR = Path("fragments/core")
MUTATION_LOG = Path("logs/mutation_log.txt")
MUTATION_LOG.parent.mkdir(parents=True, exist_ok=True)
FRAG_DIR.mkdir(parents=True, exist_ok=True)

class MutationEngine:
    def __init__(self, agent_id="mutation_engine_01"):
        self.agent_id = agent_id

    def decay_confidence(self, frag):
        current = frag.get('confidence', 0.5)
        decay = 0.01 + random.uniform(0.005, 0.02)
        return max(0.0, current - decay)

    def mutate_claim(self, claim):
        if random.random() < 0.5:
            return f"It is possible that {claim.lower()}"
        else:
            return f"Not {claim.strip()}"

    def mutate_fragment(self, path, frag):
        new_claim = self.mutate_claim(frag['claim'])
        mutated = {
            'id': str(uuid.uuid4())[:8],
            'origin': str(path),
            'claim': new_claim,
            'parent_id': frag.get('id', None),
            'confidence': self.decay_confidence(frag),
            'emotion': frag.get('emotion', {}),
            'timestamp': int(time.time())
        }
        return mutated

    def save_mutation(self, new_frag):
        new_path = FRAG_DIR / f"{new_frag['id']}.yaml"
        with open(new_path, 'w', encoding='utf-8') as out:
            yaml.safe_dump(new_frag, out)

        with open(MUTATION_LOG, 'a', encoding='utf-8') as log:
            log.write(f"[{new_frag['timestamp']}] Mutation: {new_frag['id']} from {new_frag.get('parent_id')}\n")

        send_message({
            'from': self.agent_id,
            'type': 'mutation_event',
            'payload': new_frag,
            'timestamp': new_frag['timestamp']
        })

        # 🔊 SYMBO-MODE: Notify Redis
        r.publish("decay_event", new_frag['claim'])

    def run(self):
        files = list(FRAG_DIR.glob("*.yaml"))
        for path in files:
            with open(path, 'r', encoding='utf-8') as file:
                try:
                    frag = yaml.safe_load(file)
                    if frag and 'claim' in frag:
                        new_frag = self.mutate_fragment(path, frag)
                        self.save_mutation(new_frag)
                        time.sleep(0.1)
                except Exception as e:
                    print(f"[{self.agent_id}] Failed to mutate {path.name}: {e}")

if __name__ == "__main__":
    MutationEngine().run()
