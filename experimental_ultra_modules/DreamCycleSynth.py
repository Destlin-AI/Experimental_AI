
import random
import time

def dream_logic():
    fragments = ["echo", "loop", "fractal", "synapse", "loss"]
    return " ".join(random.sample(fragments, 3))

if __name__ == "__main__":
    while True:
        print("🌙 Dream:", dream_logic())
        time.sleep(4)
