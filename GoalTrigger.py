
# === MODULE: GoalTrigger ===

from datetime import datetime
from pathlib import Path
import uuid
import yaml

class GoalTrigger:
    def __init__(self, path='D:/Project_AI/fragments/goals'):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)

    def propose(self, description, urgency=0.5, agent='swarm_manager'):
        goal_id = str(uuid.uuid4())
        goal = {
            'id': goal_id,
            'description': description,
            'urgency': urgency,
            'origin': agent,
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'proposed'
        }
        with open(self.path / f"{goal_id}.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(goal, f)
        print(f"[🎯] Goal proposed: {description[:40]}...")
