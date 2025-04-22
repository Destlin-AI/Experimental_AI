
# === MODULE: RuntimeMonitorAgent ===

import time

class RuntimeMonitorAgent:
    def __init__(self):
        self.events = []

    def log_event(self, msg, level="info"):
        self.events.append((time.time(), level.upper(), msg))
        print(f"[🕵️‍♂️] [{level.upper()}] {msg}")

    def recent(self, n=5):
        return self.events[-n:]
