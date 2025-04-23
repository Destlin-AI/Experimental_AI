# fragment_decay_engine.py
# 🔥 Symbolic fragment rot system
# Rewrites fragment metadata to simulate aging, decay, and drift

import os
import yaml
import random
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# === CORE TRUTH ===
CORE_AXIOM = {
    "claim": "Something must stay still so everything else can move.",
    "role": "axiom",
    "immutable": True
}

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

# Simulated timing feedback
SIMULATED_TIMERS = {
    "fan_rpm": lambda: random.uniform(0.85, 1.15),
    "spin_drive_latency": lambda: random.uniform(0.75, 1.25)
}

def get_decay_multiplier():
    # Average the simulated timing influence
    modifiers = [fn() for fn in SIMULATED_TIMERS.values()]
    return sum(modifiers) / len(modifiers)


def should_decay(file_path):
    modified = datetime.fromtimestamp(file_path.stat().st_mtime)
    return datetime.now() - modified > timedelta(days=DECAY_AGE_DAYS)


def decay_fragment(frag):
    if not isinstance(frag, dict):
        return frag

    # Skip axiom
    if frag.get("claim") == CORE_AXIOM["claim"]:
        frag["immutable"] = True
        return frag

    multiplier = get_decay_multiplier()

    # Apply decay rules
    for field, fn in DECAY_RULES.items():
        if field in frag:
            frag[field] = fn(frag[field] * multiplier)

    # Simulate drift
    frag = shuffle_fields(frag)
    frag['decayed'] = True
    frag['decay_timestamp'] = datetime.now().isoformat()
    frag['decay_modifier'] = round(multiplier, 3)
    return frag


def process_single_fragment(path):
    if should_decay(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            decayed = decay_fragment(data)
            out_path = DECAYED_PATH / path.name
            with open(out_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(decayed, f, sort_keys=False)
            print(f"🧪 Decayed: {path.name} -> {out_path.name}")
        except Exception as e:
            print(f"WARNING  Failed to process {path.name}: {e}")


async def process_fragments():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as executor:
        tasks = []
        for path in FRAGMENTS_PATH.rglob("*.yaml"):
            tasks.append(loop.run_in_executor(executor, process_single_fragment, path))
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    print("INFO Starting fragment decay scan (async)...")
    asyncio.run(process_fragments())
    print("[OK] Decay cycle complete.")
