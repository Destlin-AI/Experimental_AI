# === BATCH 8: fragment_feedback_loop.py ===

import yaml
import uuid
from pathlib import Path
from datetime import datetime

FRAG_DIR = Path("D:/Project_AI/fragments/feedback")
FRAG_DIR.mkdir(parents=True, exist_ok=True)

def log_feedback_response(response_text, tags=None, origin="feedback_loop", subcat="meta"):
    frag_id = str(uuid.uuid4())
    frag = {
        "id": frag_id,
        "claim": response_text.strip(),
        "sub_category": subcat,
        "confidence": 0.95,
        "tags": tags or ["feedback"],
        "origin": origin,
        "filepath": str(FRAG_DIR / f"{frag_id}.yaml"),
        "timestamp": datetime.utcnow().isoformat(),
        "content": response_text.strip()
    }
    with open(FRAG_DIR / f"{frag_id}.yaml", 'w', encoding='utf-8') as f:
        yaml.dump(frag, f)
    print(f"[🔁] Feedback loop fragment stored: {frag_id}")
    return frag

if __name__ == "__main__":
    log_feedback_response("Model determined that fragment confidence was too low.", tags=["flag", "confidence"])
