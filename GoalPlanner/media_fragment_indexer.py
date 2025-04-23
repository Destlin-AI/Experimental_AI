# === BATCH 9: media_fragment_indexer.py ===

import os
import uuid
import yaml
import pytesseract
from PIL import Image
from pathlib import Path
from datetime import datetime

MEDIA_DIR = Path("D:/Project_AI/media/image")
FRAG_DIR = Path("D:/Project_AI/fragments/media")
FRAG_DIR.mkdir(parents=True, exist_ok=True)

def image_to_fragment(img_path):
    try:
        img = Image.open(img_path)
        text = pytesseract.image_to_string(img)
        if not text.strip():
            print(f"[⚠️] No text found in: {img_path.name}")
            return None

        fid = str(uuid.uuid4())
        frag = {
            "id": fid,
            "claim": text.strip(),
            "sub_category": "ocr",
            "confidence": 0.88,
            "tags": ["ocr", "image"],
            "origin": "media_indexer",
            "filepath": str(FRAG_DIR / f"{fid}.yaml"),
            "timestamp": datetime.utcnow().isoformat(),
            "content": text.strip()
        }

        with open(FRAG_DIR / f"{fid}.yaml", "w", encoding="utf-8") as f:
            yaml.dump(frag, f)

        print(f"[🖼️] Fragment indexed from {img_path.name}")
        return frag

    except Exception as e:
        print(f"[❌] Failed to OCR {img_path.name}: {e}")
        return None

def index_all_images():
    for img_file in MEDIA_DIR.glob("*.png"):
        image_to_fragment(img_file)
    for img_file in MEDIA_DIR.glob("*.jpg"):
        image_to_fragment(img_file)

if __name__ == "__main__":
    index_all_images()
