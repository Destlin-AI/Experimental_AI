"""
LOGICSHREDDER :: total_devourer.py
Purpose: Consume .txt, .json, .yaml, .py from logic_input/, convert to symbolic logic, store in fragments/core
"""

import os, uuid, yaml, json, re, shutil
from pathlib import Path
import time

INPUT_DIR = Path("logic_input")
CONSUMED_DIR = INPUT_DIR / "devoured"
FRAG_DIR = Path("fragments/core")
DISPATCH_DIR = Path("fragments/incoming")

INPUT_DIR.mkdir(exist_ok=True)
CONSUMED_DIR.mkdir(exist_ok=True)
FRAG_DIR.mkdir(parents=True, exist_ok=True)
DISPATCH_DIR.mkdir(parents=True, exist_ok=True)

def is_valid_sentence(line):
    if not line or len(line) < 10: return False
    if line.count(" ") < 2: return False
    if re.match(r'^[\d\W_]+$', line): return False
    return True

def sanitize(line):
    return line.strip().strip("\"',.;:").replace("”", "").replace("“", "")

def extract_claims_txt(f):
    return [sanitize(l) for l in open(f, 'r', encoding='utf-8') if is_valid_sentence(sanitize(l))]

def extract_claims_json(f):
    try:
        data = json.load(open(f, 'r', encoding='utf-8'))
        if isinstance(data, list):
            return [sanitize(item) for item in data if isinstance(item, str) and is_valid_sentence(item)]
        if isinstance(data, dict):
            return [sanitize(v) for k, v in data.items() if isinstance(v, str) and is_valid_sentence(v)]
    except: pass
    return []

def extract_claims_yaml(f):
    try:
        data = yaml.safe_load(open(f, 'r', encoding='utf-8'))
        if isinstance(data, list):
            return [sanitize(item) for item in data if isinstance(item, str) and is_valid_sentence(item)]
        if isinstance(data, dict):
            return [sanitize(v) for k, v in data.items() if isinstance(v, str) and is_valid_sentence(v)]
    except: pass
    return []

def extract_claims_py(f):
    lines = []
    for line in open(f, 'r', encoding='utf-8'):
        if is_valid_sentence(line) and any(k in line for k in ["def ", "return", "==", "if "]):
            lines.append(sanitize(line))
    return lines

def write_fragment(claim, origin):
    frag = {
        "id": str(uuid.uuid4())[:8],
        "claim": claim,
        "confidence": 0.8,
        "emotion": {},
        "timestamp": int(time.time()),
        "source": origin
    }
    core_path = FRAG_DIR / f"{frag['id']}.yaml"
    dist_path = DISPATCH_DIR / f"{frag['id']}.yaml"
    for p in [core_path, dist_path]:
        with open(p, 'w', encoding='utf-8') as f:
            yaml.safe_dump(frag, f)

def devour():
    files = list(INPUT_DIR.glob("*.*"))
    total = 0
    for f in files:
        claims = []
        ext = f.suffix.lower()
        if ext == ".txt":
            claims = extract_claims_txt(f)
        elif ext == ".json":
            claims = extract_claims_json(f)
        elif ext == ".yaml":
            claims = extract_claims_yaml(f)
        elif ext == ".py":
            claims = extract_claims_py(f)
        elif ext in [".gguf", ".safetensors", ".bin"]:
            print(f"[devourer] 🧊 Skipped binary model: {f.name}")
            continue

        if claims:
            for c in claims:
                write_fragment(c, f.name)
            print(f"[devourer] [OK] Ingested {len(claims)} from {f.name}")
            total += len(claims)
            shutil.move(f, CONSUMED_DIR / f.name)
        else:
            print(f"[devourer] WARNING Skipped {f.name} (no valid claims)")

    print(f"[devourer] 🔥 Total logic extracted: {total}")

if __name__ == "__main__":
    devour()
