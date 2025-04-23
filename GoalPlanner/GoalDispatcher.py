
# === MODULE: GoalDispatcher ===

import json
from pathlib import Path
from datetime import datetime

class GoalDispatcher:
    def __init__(self, dispatch_log='D:/Project_AI/logs/goal_dispatch.jsonl'):
        self.log_path = Path(dispatch_log)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            self.log_path.write_text("", encoding='utf-8')

    def dispatch(self, goal_obj, agent_name):
        record = {
            "goal_id": goal_obj.get("id"),
            "agent": agent_name,
            "description": goal_obj.get("description"),
            "timestamp": datetime.utcnow().isoformat(),
            "status": "dispatched"
        }
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record) + "\n")
        print(f"[📨] Dispatched goal to {agent_name}: {goal_obj.get('description')}")
        return record
