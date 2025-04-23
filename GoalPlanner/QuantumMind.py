# === MODULE: QuantumMind ===

import numpy as np
from scipy.linalg import expm

class QuantumMind:
    def __init__(self, q=8):
        self.q = q
        self.H = np.tensordot(np.random.randn(2**q, 2**q), np.eye(2**q)*1j, 1)
        self.W = np.random.rand(2**q)
        self.active = False

    def toggle(self, state: bool):
        self.active = state
        print(f"[🔘] QuantumMind {'activated' if state else 'deactivated'}")

    def perceive(self, data):
        if not self.active:
            print("[⚠️] QuantumMind is inactive.")
            return data
        norm_data = data / np.linalg.norm(data)
        return expm(-1j * self.H) @ norm_data

    def think(self, perceived):
        if not self.active:
            return perceived
        return np.fft.irfft(self.W * np.fft.rfft(perceived))

    def evolve(self):
        if not self.active:
            return
        evolved = self.think(self.perceive(self.H))
        self.W = np.abs(evolved)
        self.H = np.tensordot(self.H, np.diag(self.W), 1)
        print("[🧠] QuantumMind evolved.")

# Usage:
# qm = QuantumMind()
# qm.toggle(True)
# qm.evolve()
# output = qm.think(qm.perceive(np.random.rand(2**8)))
