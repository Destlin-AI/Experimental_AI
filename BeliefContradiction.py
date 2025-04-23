
# === MODULE: BeliefContradiction ===

import json
from pathlib import Path
from datetime import datetime

class BeliefContradiction:
    def __init__(self, contradiction_log='D:/Project_AI/logs/contradictions.jsonl'):
        self.log_path = Path(contradiction_log)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            self.log_path.write_text("", encoding='utf-8')

    def flag(self, belief_a, belief_b, agent='belief_watcher'):
        contradiction = {
            "a": belief_a,
            "b": belief_b,
            "timestamp": datetime.utcnow().isoformat(),
            "agent": agent
        }
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(contradiction) + "\n")
        print(f"[⚠️] Contradiction flagged between: '{belief_a[:30]}...' and '{belief_b[:30]}...'")
