
# === MODULE: GoalManagerQueue ===

import json
import uuid
from datetime import datetime
from pathlib import Path

class GoalManagerQueue:
    def __init__(self, queue_path='D:/Project_AI/meta/goal_queue.json'):
        self.path = Path(queue_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding='utf-8')

    def enqueue(self, description, urgency=0.5, agent='scheduler'):
        q = json.loads(self.path.read_text(encoding='utf-8'))
        goal = {
            "id": str(uuid.uuid4()),
            "description": description,
            "urgency": urgency,
            "agent": agent,
            "timestamp": datetime.utcnow().isoformat()
        }
        q.append(goal)
        self.path.write_text(json.dumps(q, indent=2), encoding='utf-8')
        print(f"[🚀] Enqueued goal: {description[:40]}...")

    def dequeue(self):
        q = json.loads(self.path.read_text(encoding='utf-8'))
        if not q:
            print("[🛑] No goals to dequeue.")
            return None
        top = q.pop(0)
        self.path.write_text(json.dumps(q, indent=2), encoding='utf-8')
        print(f"[✅] Dequeued goal: {top['description']}")
        return top
