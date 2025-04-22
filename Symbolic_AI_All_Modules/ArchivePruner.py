
# === MODULE: ArchivePruner ===

import duckdb
from pathlib import Path

class ArchivePruner:
    def __init__(self, db_root='D:/Project_AI/memory_db'):
        self.db_root = Path(db_root)

    def prune(self, days_old=30):
        for db_path in self.db_root.glob("*.duckdb"):
            try:
                conn = duckdb.connect(str(db_path))
                conn.execute(f"DELETE FROM fragments WHERE timestamp < NOW() - INTERVAL '{days_old} days'")
                conn.close()
                print(f"[🧹] Pruned {db_path.name} entries older than {days_old} days")
            except Exception as e:
                print(f"[⚠️] Failed to prune {db_path.name}: {e}")
