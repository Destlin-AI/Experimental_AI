import os
import yaml
from pathlib import Path

LAYER_MAP_PATH = Path("subcon_map.yaml")
FRAGMENTS_DIR = Path("fragments/core")
OUTPUT_PATH = Path("meta/subcon_layer_cache.yaml")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

class SubconLayerMapper:
    def __init__(self):
        self.layer_map = self.load_map()

    def load_map(self):
        if not LAYER_MAP_PATH.exists():
            print("[Mapper] No layer map found. Returning empty.")
            return {}
        with open(LAYER_MAP_PATH, 'r') as f:
            return yaml.safe_load(f)

    def extract_links(self):
        results = {}
        for file in FRAGMENTS_DIR.glob("*.yaml"):
            try:
                with open(file, 'r') as f:
                    frag = yaml.safe_load(f)
                tags = frag.get("tags", [])
                for tag in tags:
                    if tag in self.layer_map:
                        results.setdefault(tag, []).append(frag['id'])
            except Exception as e:
                print(f"[Mapper] Failed to read {file.name}: {e}")
        return results

    def save_cache(self, data):
        with open(OUTPUT_PATH, 'w') as out:
            yaml.dump(data, out)
        print(f"[Mapper] Saved subcon layer associations -> {OUTPUT_PATH}")

    def run(self):
        links = self.extract_links()
        self.save_cache(links)

if __name__ == "__main__":
    mapper = SubconLayerMapper()
    mapper.run()
