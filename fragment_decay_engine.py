# fragment_decay_engine.py
# 🔥 Symbolic fragment rot system
# Rewrites fragment metadata to simulate aging, decay, and drift

import os
import yaml
import random
from datetime import datetime, timedelta
from pathlib import Path

# Configurable decay rules
DECAY_RULES = {
    "certainty": lambda x: max(0.0, round(x - random.uniform(0.05, 0.2), 3)),
    "urgency": lambda x: max(0.0, round(x - random.uniform(0.01, 0.05), 3)),
    "doubt": lambda x: min(1.0, round(x + random.uniform(0.05, 0.2), 3)),
    "confidence": lambda x: max(0.0, round(x - random.uniform(0.1, 0.3), 3))
}

# Optional field shuffler
def shuffle_fields(fragment):
    if 'claim' in fragment and random.random() < 0.4:
        fragment['claim'] = f"[fragmented] {fragment['claim']}"
    if 'tags' in fragment and isinstance(fragment['tags'], list):
        random.shuffle(fragment['tags'])
    return fragment

# Age threshold (e.g. 10 days = eligible for decay)
DECAY_AGE_DAYS = 10

# Base path for fragments
FRAGMENTS_PATH = Path("C:/Users/PC/Desktop/Operation Future/Allinonepy/fragments")

# Rot target output
DECAYED_PATH = Path("C:/Users/PC/Desktop/Operation Future/Allinonepy/fragments/decayed")
DECAYED_PATH.mkdir(parents=True, exist_ok=True)


def should_decay(file_path):
    modified = datetime.fromtimestamp(file_path.stat().st_mtime)
    return datetime.now() - modified > timedelta(days=DECAY_AGE_DAYS)


def decay_fragment(frag):
    if not isinstance(frag, dict):
        return frag

    # Apply decay rules
    for field, fn in DECAY_RULES.items():
        if field in frag:
            frag[field] = fn(frag[field])

    # Simulate drift
    frag = shuffle_fields(frag)
    frag['decayed'] = True
    frag['decay_timestamp'] = datetime.now().isoformat()
    return frag


def process_fragments():
    for path in FRAGMENTS_PATH.rglob("*.yaml"):
        if should_decay(path):
            with open(path, 'r', encoding='utf-8') as f:
                try:
                    data = yaml.safe_load(f)
                except yaml.YAMLError:
                    continue
            decayed = decay_fragment(data)
            out_path = DECAYED_PATH / path.name
            with open(out_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(decayed, f, sort_keys=False)
            print(f"🧪 Decayed: {path.name} -> {out_path.name}")


if __name__ == "__main__":
    print("INFO Starting fragment decay scan...")
    process_fragments()
    print("[OK] Decay cycle complete.")
