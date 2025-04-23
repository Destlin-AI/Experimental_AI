# === MODULE: CodeImmuneSystem ===

import hashlib
from pathlib import Path

class CodeImmuneSystem:
    def __init__(self, quarantine_path='D:/Project_AI/fragments/quarantine'):
        self.seen_hashes = set()
        self.quarantine_path = Path(quarantine_path)
        self.quarantine_path.mkdir(parents=True, exist_ok=True)

    def _hash(self, code):
        return hashlib.sha256(code.encode()).hexdigest()

    def scan(self, code):
        h = self._hash(code)
        if h in self.seen_hashes:
            print(f"[🛡️] Duplicate or flagged code detected. Immune system engaged.")
            self._quarantine(code, h)
            return False
        self.seen_hashes.add(h)
        print("[✅] Code passed immune check.")
        return True

    def _quarantine(self, code, h):
        qfile = self.quarantine_path / f"quarantine_{h[:8]}.txt"
        qfile.write_text(code, encoding='utf-8')
        print(f"[🧬] Quarantined to: {qfile.name}")

# Usage:
# cis = CodeImmuneSystem()
# cis.scan("print('Hello World')")
# cis.scan("print('Hello World')")
