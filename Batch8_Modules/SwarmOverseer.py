
# === MODULE: SwarmOverseer ===

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
