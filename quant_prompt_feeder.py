# quant_prompt_feeder.py
# Uses a local .gguf model to generate beliefs and feed the LogicShredder

import subprocess
import time
from pathlib import Path

MODEL_PATH = Path("models/TinyLlama.Q4_0.gguf")  # CHANGE if different
LLAMA_CPP_PATH = Path("llama.cpp/build/bin/main")  # Point to llama.cpp binary
PROMPT = "List 25 fundamental beliefs about the universe, logic, and consciousness."
OUTPUT_FILE = Path("logic_input/generated_beliefs.txt")

def generate_beliefs():
    print(f"[feeder] INFO Generating beliefs using {MODEL_PATH.name}")
    with open("prompt.txt", "w", encoding="utf-8") as f:
        f.write(PROMPT)

    try:
        result = subprocess.run([
            str(LLAMA_CPP_PATH),
            "-m", str(MODEL_PATH),
            "-p", PROMPT,
            "--n-predict", "300",
            "--top-k", "40",
            "--top-p", "0.9",
            "--temp", "0.7"
        ], capture_output=True, text=True, timeout=120)

        if result.returncode == 0:
            text = result.stdout
            with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
                out.write(text)
            print(f"[feeder] [OK] Beliefs saved to {OUTPUT_FILE}")
        else:
            print(f"[feeder] ERROR Model failed to respond properly.")

    except Exception as e:
        print(f"[feeder] ERROR Model execution failed: {e}")

def feed_beliefs():
    print("[feeder] 🔄 Feeding into LogicShredder...")
    subprocess.run(["python", "total_devourer.py"])
    subprocess.run(["python", "run_logicshredder.py"])

if __name__ == "__main__":
    generate_beliefs()
    time.sleep(1)
    feed_beliefs()
