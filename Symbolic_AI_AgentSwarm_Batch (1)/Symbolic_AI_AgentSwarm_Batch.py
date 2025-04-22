# === AGENT SWARM CORE MODULES ===

# SwarmOverseer: agent dispatcher
class SwarmOverseer:
    def __init__(self):
        self.agents = {}

    def register(self, name, fn):
        self.agents[name] = fn
        print(f"[🛰️] Registered swarm agent: {name}")

    def dispatch(self, name, task):
        if name in self.agents:
            print(f"[📡] Dispatching to {name}: {task}")
            return self.agents[name](task)
        print(f"[❌] Agent '{name}' not found.")
        return None

# ArchivePruner: memory cleaner
import duckdb
from pathlib import Path

class ArchivePruner:
    def __init__(self, db_root='D:/Project_AI/memory_db'):
        self.db_root = Path(db_root)

    def prune(self, days_old=30):
        for db_path in self.db_root.glob("*.duckdb"):
            try:
                conn = duckdb.connect(str(db_path))
                conn.execute(f"DELETE FROM fragments WHERE timestamp < NOW() - INTERVAL '{days_old} days'")
                conn.close()
                print(f"[🧹] Pruned {db_path.name} entries older than {days_old} days")
            except Exception as e:
                print(f"[⚠️] Failed to prune {db_path.name}: {e}")

# RuntimeMonitorAgent: stability checker
import time

class RuntimeMonitorAgent:
    def __init__(self):
        self.events = []

    def log_event(self, msg, level="info"):
        self.events.append((time.time(), level.upper(), msg))
        print(f"[🕵️‍♂️] [{level.upper()}] {msg}")

    def recent(self, n=5):
        return self.events[-n:]
