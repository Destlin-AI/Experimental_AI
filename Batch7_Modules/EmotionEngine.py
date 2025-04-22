# === MODULE: EmotionEngine ===

class EmotionEngine:
    def __init__(self):
        self.valence = 0.0   # pleasure / displeasure
        self.arousal = 0.0   # excitement / calm
        self.saturation = 0.0  # emotional load

    def update(self, signal_strength, polarity):
        self.arousal = min(1.0, max(0.0, self.arousal + signal_strength * 0.1))
        self.valence = min(1.0, max(-1.0, self.valence + polarity * 0.1))
        self.saturation = min(1.0, self.saturation + abs(signal_strength * polarity) * 0.2)
        print(f"[💓] Emotion updated: valence={self.valence:.2f}, arousal={self.arousal:.2f}, saturation={self.saturation:.2f}")

    def decay(self, rate=0.01):
        self.arousal *= (1 - rate)
        self.saturation *= (1 - rate)
        print(f"[💤] Emotional decay applied.")

    def state(self):
        return {
            "valence": round(self.valence, 3),
            "arousal": round(self.arousal, 3),
            "saturation": round(self.saturation, 3),
        }
