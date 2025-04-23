# === MODULE: SchrödExperiment ===

import random
from datetime import datetime

class SchrödExperiment:
    def __init__(self):
        self.memory = {}
        self.history = []

    def inject_belief(self, key, value):
        self.memory[key] = {"state": "undecided", "value": value, "timestamp": datetime.utcnow()}
        print(f"[🐱] Injected undecided belief: {key} → ?")

    def observe(self, key):
        if key not in self.memory:
            print(f"[❌] No such belief to observe: {key}")
            return None
        entry = self.memory[key]
        if entry["state"] == "undecided":
            if random.random() > 0.5:
                entry["state"] = "true"
            else:
                entry["state"] = "false"
            print(f"[📡] Observation collapsed: {key} → {entry['state']}")
        else:
            print(f"[📁] Already observed: {key} → {entry['state']}")
        return entry["state"]

# Usage:
# se = SchrödExperiment()
# se.inject_belief("ghost_in_code", "anomaly")
# print(se.observe("ghost_in_code"))
