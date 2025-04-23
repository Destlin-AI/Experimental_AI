"""
LOGICSHREDDER :: logic_scraper_dispatch.py
Purpose: Auto-detects file types in /llm_output/, routes to correct scraper, feeds fragments to core
"""

import os, uuid, yaml, json, re, shutil
from pathlib import Path
import time

SRC_DIR = Path("llm_output")
CONSUMED_DIR = SRC_DIR / "devoured"
FRAG_DIR = Path("fragments/core")

SRC_DIR.mkdir(exist_ok=True)
CONSUMED_DIR.mkdir(exist_ok=True)
FRAG_DIR.mkdir(parents=True, exist_ok=True)

def is_valid_sentence(line):
    if not line or len(line) < 10: return False
    if line.count(" ") < 2: return False
    if re.match(r'^[\d\W_]+$', line): return False
    return True

def sanitize(line):
    return line.strip().strip("\"',.;:").replace("”", "").replace("“", "")

def extract_txt(path):
    return [sanitize(l) for l in open(path, 'r', encoding='utf-8') if is_valid_sentence(sanitize(l))]

def extract_json(path):
    try:
        data = json.load(open(path, 'r', encoding='utf-8'))
        if isinstance(data, list):
            return [sanitize(item) for item in data if isinstance(item, str) and is_valid_sentence(item)]
        if isinstance(data, dict):
            return [sanitize(v) for k, v in data.items() if isinstance(v, str) and is_valid_sentence(v)]
    except: pass
    return []

def extract_yaml(path):
    try:
        data = yaml.safe_load(open(path, 'r', encoding='utf-8'))
        if isinstance(data, list):
            return [sanitize(item) for item in data if isinstance(item, str) and is_valid_sentence(item)]
        if isinstance(data, dict):
            return [sanitize(v) for k, v in data.items() if isinstance(v, str) and is_valid_sentence(v)]
    except: pass
    return []

def extract_py(path):
    lines = []
    for line in open(path, 'r', encoding='utf-8'):
        if is_valid_sentence(line) and any(k in line for k in ["def ", "return", "==", "if "]):
            lines.append(sanitize(line))
    return lines

def write_fragment(claim, source):
    frag = {
        "id": str(uuid.uuid4())[:8],
        "claim": claim,
        "confidence": 0.85,
        "emotion": {},
        "timestamp": int(time.time()),
        "source": source
    }
    path = FRAG_DIR / f"{frag['id']}.yaml"
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(frag, f)

def dispatch():
    files = list(SRC_DIR.glob("*.*"))
    total = 0
    for f in files:
        claims = []
        ext = f.suffix.lower()
        if ext == ".txt":
            claims = extract_txt(f)
        elif ext == ".json":
            claims = extract_json(f)
        elif ext == ".yaml":
            claims = extract_yaml(f)
        elif ext == ".py":
            claims = extract_py(f)
        elif ext in [".gguf", ".bin", ".safetensors"]:
            print(f"[dispatcher] WARNING Skipped binary: {f.name}")
            continue

        if claims:
            for c in claims:
                write_fragment(c, f.name)
            print(f"[dispatcher] [OK] Routed {len(claims)} from {f.name}")
            total += len(claims)
            shutil.move(f, CONSUMED_DIR / f.name)
        else:
            print(f"[dispatcher] WARNING No usable logic in {f.name}")

    print(f"[dispatcher] 🔁 Total symbolic fragments created: {total}")

if __name__ == "__main__":
    dispatch()
