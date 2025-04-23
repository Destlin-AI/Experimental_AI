import yaml
from pathlib import Path
from datetime import datetime

INDEX = Path("meta/memory_index.yaml")
OUT = Path("meta/memory_visual_report.txt")

def load_index():
    with open(INDEX, 'r') as f:
        return yaml.safe_load(f)

def make_heatbar(conf):
    filled = int(conf * 20)
    return "█" * filled + "-" * (20 - filled)

def dump_visual():
    data = load_index()
    lines = [f"INFO MEMORY VISUALIZER REPORT – {datetime.now().isoformat()}"]
    for fid, meta in sorted(data.items()):
        conf = meta.get('confidence', 0.5)
        last = meta.get('last_seen', '—')
        lines.append(f"{fid}: {make_heatbar(conf)} | Confidence: {conf:.2f} | Last Seen: {last} | Status: {meta.get('status', 'unknown')}")
    with open(OUT, 'w') as f:
        f.write("\n".join(lines))
    print(f"[memory_visualizer] Output -> {OUT}")

if __name__ == "__main__":
    dump_visual()
