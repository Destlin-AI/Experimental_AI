# === MODULE: AgentUsageLogger ===

import json
from datetime import datetime
from pathlib import Path

class AgentUsageLogger:
    def __init__(self, log_path='D:/Project_AI/logs/agent_trace.jsonl'):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            self.log_path.write_text("", encoding='utf-8')

    def log(self, agent_name, task, result=None):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": agent_name,
            "task": task,
            "result": result
        }
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + "\n")
        print(f"[📓] Logged task for {agent_name}: {task}")
