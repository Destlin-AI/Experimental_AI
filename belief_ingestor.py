"""
LOGICSHREDDER :: belief_ingestor.py
Purpose: Scans feedbox/ for .txt/.json/.yaml/.py files, extracts claims, converts to fragment YAMLs
"""

import os, uuid, yaml, json
from pathlib import Path
import time

FEED_DIR = Path("feedbox")
CONSUMED_DIR = FEED_DIR / "consumed"
FRAG_DIR = Path("fragments/core")

FEED_DIR.mkdir(exist_ok=True)
CONSUMED_DIR.mkdir(exist_ok=True)
FRAG_DIR.mkdir(parents=True, exist_ok=True)

def extract_claims_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip("- ").strip() for line in f.readlines() if line.strip()]
    return [line for line in lines if len(line) > 5]

def extract_claims_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            return [str(item).strip() for item in data if isinstance(item, str)]
        return []
    except:
        return []

def extract_claims_from_yaml(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        if isinstance(data, list):
            return [str(item).strip() for item in data if isinstance(item, str)]
        return []
    except:
        return []

def extract_claims_from_py(file_path):
    lines = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if "==" in line or "def " in line or "return" in line:
                lines.append(line.strip())
    return lines

def write_fragment(claim):
    frag = {
        "id": str(uuid.uuid4())[:8],
        "claim": claim,
        "confidence": 0.85,
        "emotion": {},
        "timestamp": int(time.time())
    }
    fpath = FRAG_DIR / f"{frag['id']}.yaml"
    with open(fpath, 'w', encoding='utf-8') as f:
        yaml.safe_dump(frag, f)

def ingest_feedbox():
    files = list(FEED_DIR.glob("*.*"))
    total_claims = 0

    for file_path in files:
        claims = []
        ext = file_path.suffix.lower()

        if ext == ".txt":
            claims = extract_claims_from_txt(file_path)
        elif ext == ".json":
            claims = extract_claims_from_json(file_path)
        elif ext == ".yaml":
            claims = extract_claims_from_yaml(file_path)
        elif ext == ".py":
            claims = extract_claims_from_py(file_path)

        if claims:
            for claim in claims:
                write_fragment(claim)
            file_path.rename(CONSUMED_DIR / file_path.name)
            print(f"[ingestor] [OK] Ingested {len(claims)} from {file_path.name}")
            total_claims += len(claims)
        else:
            print(f"[ingestor] WARNING Skipped {file_path.name} (no claims)")

    print(f"[ingestor] INFO Total beliefs ingested: {total_claims}")

if __name__ == "__main__":
    ingest_feedbox()
