# quant_feeder_setup.py
# Fully automated setup for quant_prompt_feeder

import subprocess
import os
from pathlib import Path
import sys
import time
import urllib.request
import zipfile

LLAMA_REPO = "https://github.com/ggerganov/llama.cpp.git"
MODEL_URL = "https://huggingface.co/afrideva/Tinystories-gpt-0.1-3m-GGUF/resolve/main/TinyStories-GPT-0.1-3M.Q2_K.gguf"

MODEL_DIR = Path("models")
MODEL_FILE = MODEL_DIR / "TinyStories.Q2_K.gguf"
LLAMA_DIR = Path("llama.cpp")
LLAMA_BIN = LLAMA_DIR / "build/bin/main"

def install_dependencies():
    print("[setup] CONFIG Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "--upgrade", "pip"])
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "requests"])

def clone_llama_cpp():
    if not LLAMA_DIR.exists():
        print("[setup] INFO Cloning llama.cpp...")
        subprocess.run(["git", "clone", LLAMA_REPO])
    else:
        print("[setup] [OK] llama.cpp already exists")

def build_llama_cpp():
    print("[setup] 🔨 Building llama.cpp...")
    os.makedirs(LLAMA_DIR / "build", exist_ok=True)
    subprocess.run(["cmake", "-B", "build"], cwd=LLAMA_DIR)
    subprocess.run(["cmake", "--build", "build", "--config", "Release"], cwd=LLAMA_DIR)

def download_model():
    if MODEL_FILE.exists():
        print(f"[setup] [OK] Model already downloaded: {MODEL_FILE.name}")
        return
    print(f"[setup] ⬇️  Downloading model to {MODEL_FILE}...")
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(MODEL_URL, MODEL_FILE)

def patch_feeder():
    print("[setup] 🛠️ Patching quant_prompt_feeder.py with model and llama path")
    feeder_code = Path("quant_prompt_feeder.py").read_text(encoding="utf-8")
    patched = feeder_code.replace(
        'MODEL_PATH = Path("models/TinyLlama.Q4_0.gguf")',
        f'MODEL_PATH = Path("{MODEL_FILE.as_posix()}")'
    ).replace(
        'LLAMA_CPP_PATH = Path("llama.cpp/build/bin/main")',
        f'LLAMA_CPP_PATH = Path("{LLAMA_BIN.as_posix()}")'
    )
    Path("quant_prompt_feeder.py").write_text(patched, encoding="utf-8")

def run_feeder():
    print("[setup] LAUNCH Running quant_prompt_feeder.py...")
    subprocess.run(["python", "quant_prompt_feeder.py"])

if __name__ == "__main__":
    install_dependencies()
    clone_llama_cpp()
    build_llama_cpp()
    download_model()
    patch_feeder()
    run_feeder()
