# === MODULE: SpoonEngine ===

import numpy as np
from datetime import datetime

class SpoonEngine:
    def __init__(self, base_energy=1.0):
        self.energy = base_energy
        self.decay = 0.015
        self.log = []

    def apply(self, task_importance):
        load = task_importance * self.energy
        self.energy = max(0.0, self.energy - self.decay)
        result = f"[⚙️] Load: {load:.3f}, Remaining Energy: {self.energy:.3f}"
        self.log.append((datetime.utcnow(), load, self.energy))
        print(result)
        return load

    def restore(self, amount=0.1):
        self.energy = min(1.0, self.energy + amount)
        print(f"[🔋] Energy restored: {self.energy:.3f}")

    def status(self):
        return {
            "current_energy": self.energy,
            "history": self.log[-5:],
        }

# Usage:
# se = SpoonEngine()
# se.apply(0.5)
# se.restore()
# print(se.status())
