# === MODULE: ModelStatProfiler ===

import time
import json
from pathlib import Path

class ModelStatProfiler:
    def __init__(self, log_path='D:/Project_AI/logs/model_perf.jsonl'):
        self.path = Path(log_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("", encoding='utf-8')

    def profile(self, model_name, call_fn, *args, **kwargs):
        start = time.perf_counter()
        output = call_fn(*args, **kwargs)
        end = time.perf_counter()
        elapsed = round(end - start, 4)
        stat = {
            "model": model_name,
            "time": elapsed,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        with open(self.path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(stat) + "\n")
        print(f"[📈] Profiled '{model_name}' → {elapsed}s")
        return output
