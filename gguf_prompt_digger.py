"""
LOGICSHREDDER :: gguf_prompt_digger.py
Purpose: Extract readable string chunks from .gguf binary model files, convert into belief fragments
"""

import struct
from pathlib import Path
import uuid, yaml, time

MODEL_DIR = Path("models")
FRAG_DIR = Path("fragments/core")
CONSUMED_DIR = MODEL_DIR / "parsed"

MODEL_DIR.mkdir(exist_ok=True)
FRAG_DIR.mkdir(parents=True, exist_ok=True)
CONSUMED_DIR.mkdir(exist_ok=True)

def write_fragment(claim, source):
    frag = {
        "id": str(uuid.uuid4())[:8],
        "claim": claim,
        "confidence": 0.77,
        "emotion": {},
        "timestamp": int(time.time()),
        "source": source
    }
    path = FRAG_DIR / f"{frag['id']}.yaml"
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(frag, f)

def extract_strings_from_gguf(path):
    logic_chunks = []
    try:
        with open(path, 'rb') as f:
            raw = f.read()
            strings = set()
            current = b""
            for byte in raw:
                if 32 <= byte <= 126:
                    current += bytes([byte])
                else:
                    if len(current) >= 20:
                        strings.add(current.decode(errors='ignore'))
                    current = b""
            logic_chunks = sorted(strings)
    except Exception as e:
        print(f"[gguf_digger] 💥 Failed to extract from {path.name}: {e}")
    return logic_chunks

def run_digger():
    models = list(MODEL_DIR.glob("*.gguf"))
    total = 0
    for model_path in models:
        logic = extract_strings_from_gguf(model_path)
        if logic:
            for line in logic:
                if len(line.split()) > 3 and not line.startswith("ggml"):
                    write_fragment(line.strip(), model_path.name)
            print(f"[gguf_digger] [OK] Extracted {len(logic)} strings from {model_path.name}")
            total += len(logic)
        else:
            print(f"[gguf_digger] WARNING No usable strings found in {model_path.name}")
    print(f"[gguf_digger] INFO Total beliefs extracted: {total}")

if __name__ == "__main__":
    run_digger()
