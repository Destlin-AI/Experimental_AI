
# === MODULE: NeuroStoreManager ===

import duckdb
from pathlib import Path
from datetime import datetime
import uuid
import yaml

class NeuroStoreManager:
    def __init__(self, path='D:/Project_AI/memory_db'):
        self.base = Path(path)
        self.base.mkdir(parents=True, exist_ok=True)

    def save_fragment(self, category, content, tags=None, subcat='core'):
        fid = str(uuid.uuid4())
        frag = {
            'id': fid,
            'claim': content.strip().splitlines()[0][:160],
            'sub_category': subcat,
            'confidence': 0.93,
            'tags': tags or ['core'],
            'origin': 'NeuroStore',
            'filepath': str(self.base / f'{category}.duckdb'),
            'timestamp': datetime.utcnow().isoformat(),
            'content': content.strip()
        }
        self._insert_db(category, frag)
        print(f"[🧠] Saved fragment to {category}: {fid}")

    def _insert_db(self, category, frag):
        db = self.base / f"{category}.duckdb"
        conn = duckdb.connect(str(db))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS fragments (
                id TEXT, claim TEXT, sub_category TEXT, confidence DOUBLE,
                tags TEXT[], origin TEXT, filepath TEXT, timestamp TIMESTAMP, content TEXT
            )
        """)
        conn.execute("INSERT INTO fragments VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple(frag.values()))
        conn.close()


# === MODULE: SymbolicQueryCache ===

import json
from pathlib import Path
from datetime import datetime

class SymbolicQueryCache:
    def __init__(self, path='D:/Project_AI/meta/query_cache.json'):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("{}", encoding='utf-8')

    def store(self, query, response):
        cache = json.loads(self.path.read_text(encoding='utf-8'))
        cache[query] = {
            'response': response,
            'timestamp': datetime.utcnow().isoformat()
        }
        self.path.write_text(json.dumps(cache, indent=2), encoding='utf-8')
        print(f"[💾] Cached query: '{query[:40]}...' → {len(response)} chars")

    def retrieve(self, query):
        cache = json.loads(self.path.read_text(encoding='utf-8'))
        return cache.get(query, {}).get('response')
