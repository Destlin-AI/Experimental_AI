# === MODULE: CodeMutationEngine ===

import random
from pathlib import Path
from datetime import datetime

class CodeMutationEngine:
    def __init__(self, log_path='D:/Project_AI/logs/code_mutations.jsonl'):
        self.path = Path(log_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("", encoding='utf-8')

    def mutate(self, code_block: str):
        lines = code_block.strip().splitlines()
        if not lines:
            return code_block
        idx = random.randint(0, len(lines) - 1)
        lines[idx] = "# MUTATED: " + lines[idx]
        mutated = "
".join(lines)
        self._log_mutation(code_block, mutated)
        print(f"[🧬] Mutated line {idx + 1}/{len(lines)}")
        return mutated

    def _log_mutation(self, original, mutated):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "original": original.strip()[:200],
            "mutated": mutated.strip()[:200]
        }
        with open(self.path, 'a', encoding='utf-8') as f:
            f.write(str(entry) + "
")
