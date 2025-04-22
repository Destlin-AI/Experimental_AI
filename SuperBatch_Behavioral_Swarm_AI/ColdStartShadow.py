
import pickle
import os

STATE_PATH = "coldstart_state.pkl"

def preload_memory():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "rb") as f:
            mem = pickle.load(f)
            print("🧊 Cold start memory:", mem)
    else:
        mem = {"boot": "instinct"}
        with open(STATE_PATH, "wb") as f:
            pickle.dump(mem, f)

if __name__ == "__main__":
    preload_memory()
