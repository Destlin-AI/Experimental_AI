from core.config_loader import get
"""
LOGICSHREDDER :: validator.py
Purpose: Compare symbolic beliefs, detect contradictions, write to overflow
"""

import os
import yaml
import redis
r = redis.Redis(decode_responses=True)

import time
import hashlib
import threading
import redis
from pathlib import Path

# Local module
from utils import agent_profiler

# Redis pub/sub for symbolic event broadcasts
r = redis.Redis(decode_responses=True)

# Start profiler as background daemon
threading.Thread(target=agent_profiler.run_profile_loop, daemon=True).start()


CORE_DIR = Path("fragments/core")
OVERFLOW_DIR = Path("fragments/overflow")
OVERFLOW_DIR.mkdir(parents=True, exist_ok=True)

class Validator:
    def __init__(self, agent_id="validator_01"):
        self.agent_id = agent_id
        self.frags = {}

    def hash_claim(self, claim):
        return hashlib.md5(claim.encode("utf-8")).hexdigest()

    def load_core_beliefs(self):
        for path in CORE_DIR.glob("*.yaml"):
            with open(path, 'r', encoding='utf-8') as file:
                try:
                    frag = yaml.safe_load(file)
                    if frag and 'claim' in frag:
                        claim_hash = self.hash_claim(frag['claim'])
                        self.frags[claim_hash] = (path, frag)
                except yaml.YAMLError as e:
                    print(f"[{self.agent_id}] YAML error in {path.name}: {e}")

    def contradicts(self, a, b):
        # Naive contradiction check: exact negation
        return a.lower().strip() == f"not {b.lower().strip()}"

    def run_validation(self):
        for hash_a, (path_a, frag_a) in self.frags.items():
            for hash_b, (path_b, frag_b) in self.frags.items():
                if hash_a == hash_b:
                    continue
                if self.contradicts(frag_a['claim'], frag_b['claim']):
                    contradiction_id = f"{hash_a[:6]}_{hash_b[:6]}"
                    filename = f"contradiction_{contradiction_id}.yaml"
                    contradiction_path = OVERFLOW_DIR / filename
                    if not contradiction_path.exists():
                        with open(contradiction_path, 'w', encoding='utf-8') as out:
                            yaml.safe_dump({
                                'source_1': frag_a['claim'],
                                'source_2': frag_b['claim'],
                                'path_1': str(path_a),
                                'path_2': str(path_b),
                                'detected_by': self.agent_id,
                                'timestamp': int(time.time())
                            }, out)
r.publish("contradiction_found", payload['claim_1'])  # [AUTO_EMIT]
                        send_message({
                            'from': self.agent_id,
                            'type': 'contradiction_found',
                            'payload': {
                                'claim_1': frag_a['claim'],
                                'claim_2': frag_b['claim'],
                                'paths': [str(path_a), str(path_b)]
                            },
                            'timestamp': int(time.time())
                        })

    def run(self):
        self.load_core_beliefs()
        self.run_validation()

if __name__ == "__main__":
    Validator().run()
# [CONFIG_PATCHED]