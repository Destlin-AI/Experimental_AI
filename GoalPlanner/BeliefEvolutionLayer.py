# === MODULE: BeliefEvolutionLayer ===

import json
from datetime import datetime
from pathlib import Path

class BeliefEvolutionLayer:
    def __init__(self, path="D:/Project_AI/meta/belief_evolution.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("{}", encoding="utf-8")

    def reinforce(self, belief_id):
        log = json.loads(self.path.read_text(encoding="utf-8"))
        belief = log.get(belief_id, {"count": 0, "last": None})
        belief["count"] += 1
        belief["last"] = datetime.utcnow().isoformat()
        log[belief_id] = belief
        self.path.write_text(json.dumps(log, indent=2), encoding="utf-8")
        print(f"[🔁] Reinforced belief: {belief_id} ({belief['count']})")

    def decay_all(self, rate=0.1):
        log = json.loads(self.path.read_text(encoding="utf-8"))
        for k in log:
            log[k]["count"] = max(0, round(log[k]["count"] * (1 - rate)))
        self.path.write_text(json.dumps(log, indent=2), encoding="utf-8")
        print(f"[📉] Applied decay to all beliefs.")
