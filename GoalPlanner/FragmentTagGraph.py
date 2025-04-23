
# === MODULE: FragmentTagGraph ===

import duckdb
from pathlib import Path
import matplotlib.pyplot as plt
from collections import defaultdict

class FragmentTagGraph:
    def __init__(self, db_root='D:/Project_AI/memory_db'):
        self.db_root = Path(db_root)

    def generate_tag_frequency_graph(self):
        tag_counts = defaultdict(int)
        for db_path in self.db_root.glob("*.duckdb"):
            try:
                conn = duckdb.connect(str(db_path))
                rows = conn.execute("SELECT tags FROM fragments").fetchall()
                conn.close()
                for row in rows:
                    for tag in row[0]:
                        tag_counts[tag] += 1
            except Exception as e:
                print(f"[⚠️] Error reading {db_path.name}: {e}")

        tags, counts = zip(*sorted(tag_counts.items(), key=lambda x: -x[1]))
        plt.figure(figsize=(12, 6))
        plt.bar(tags[:40], counts[:40])
        plt.title("Top Fragment Tags")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig("D:/Project_AI/meta/tag_graph.png")
        print("[📊] Tag frequency graph saved to meta/tag_graph.png")
