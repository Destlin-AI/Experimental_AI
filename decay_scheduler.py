# decay_scheduler.py
import redis
import time
from pathlib import Path
import random

r = redis.Redis(decode_responses=True)
FRAGMENTS = Path("fragments/core")

def pick_fragments(n=3):
    files = list(FRAGMENTS.glob("*.yaml"))
    return random.sample(files, min(n, len(files)))

while True:
    chosen = pick_fragments()
    for frag in chosen:
        print(f"📤 Sending {frag} to decay queue")
        r.publish("decay_queue", str(frag))
    time.sleep(10)
