
# === MODULE: GoalPlanner ===

import json
from datetime import datetime
from pathlib import Path

class GoalPlanner:
    def __init__(self, path='D:/Project_AI/meta/goal_plans.json'):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("{}", encoding='utf-8')

    def assign(self, goal_obj, steps: list[str]):
        plans = json.loads(self.path.read_text(encoding='utf-8'))
        plans[goal_obj["id"]] = {
            "description": goal_obj["description"],
            "steps": steps,
            "agent": goal_obj.get("agent", "unassigned"),
            "timestamp": datetime.utcnow().isoformat()
        }
        self.path.write_text(json.dumps(plans, indent=2), encoding='utf-8')
        print(f"[🧭] Planned {len(steps)} steps for goal: {goal_obj['description'][:40]}...")
