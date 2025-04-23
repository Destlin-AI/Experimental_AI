from core.config_loader import get
"""
LOGICSHREDDER :: guffifier_v2.py
Purpose: Ingest text files and model outputs, extract symbolic claims, write to incoming/,
         and distribute to helper modules for parallel digestion of massive models (540B and beyond)
"""

import os
import yaml
import threading
from utils import agent_profiler
# [PROFILER_INJECTED]
threading.Thread(target=agent_profiler.run_profile_loop, daemon=True).start()
from pathlib import Path
import time
import re
import uuid
import multiprocessing

IN_DIR = Path("input/")
OUT_DIR = Path("fragments/incoming")
CHUNK_DIR = Path("input/chunks")
CHUNK_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

class Guffifier:
    def __init__(self, agent_id="guffifier_01"):
        self.agent_id = agent_id

    def extract_claims(self, text):
        sentences = re.split(r'(?<=[.!?]) +', text)
        claims = [s.strip() for s in sentences if len(s.strip()) > 10]
        return claims

    def guffify(self, content, origin_path):
        claims = self.extract_claims(content)

        for claim in claims:
            fragment = {
                'id': str(uuid.uuid4())[:8],
                'origin': str(origin_path),
                'claim': claim,
                'emotion': {'neutral': 0.9},
                'confidence': 0.5,
                'timestamp': int(time.time())
            }
            out_path = OUT_DIR / f"{fragment['id']}.yaml"
            with open(out_path, 'w', encoding='utf-8') as out:
                yaml.safe_dump(fragment, out)

    def chunk_model_dump(self, path, chunk_size=50000):
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()

        base_name = path.stem
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

        for i, chunk in enumerate(chunks):
            chunk_path = CHUNK_DIR / f"{base_name}_chunk_{i}.txt"
            with open(chunk_path, 'w', encoding='utf-8') as c:
                c.write(chunk)

    def batch_chunkify(self):
        raw_files = list(IN_DIR.glob("*.txt")) + list(IN_DIR.glob("*.md")) + list(IN_DIR.glob("*.json"))
        for f in raw_files:
            self.chunk_model_dump(f)

    def worker_guffify(self, chunk_path):
        with open(chunk_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.guffify(content, chunk_path)

    def run_parallel_guffifiers(self):
        chunk_paths = list(CHUNK_DIR.glob("*.txt"))
        with multiprocessing.Pool(processes=os.cpu_count() or 4) as pool:
            pool.map(self.worker_guffify, chunk_paths)

    def run(self):
        print(f"[{self.agent_id}] Chunkifying massive model files...")
        self.batch_chunkify()
        print(f"[{self.agent_id}] Distributing to guffifier helpers...")
        self.run_parallel_guffifiers()

if __name__ == "__main__":
    Guffifier().run()
# [CONFIG_PATCHED]
