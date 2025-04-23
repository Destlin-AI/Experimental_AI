
# === MODULE: GoalReflector ===

import json
from pathlib import Path
from datetime import datetime

class GoalReflector:
    def __init__(self, path='D:/Project_AI/meta/goal_reflection.json'):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("{}", encoding='utf-8')

    def reflect(self, goal_id, success=True, notes=""):
        reflections = json.loads(self.path.read_text(encoding='utf-8'))
        reflections[goal_id] = {
            "timestamp": datetime.utcnow().isoformat(),
            "success": success,
            "notes": notes
        }
        self.path.write_text(json.dumps(reflections, indent=2), encoding='utf-8')
        print(f"[🔍] Reflected on goal {goal_id}: {'✓' if success else '✗'}")
