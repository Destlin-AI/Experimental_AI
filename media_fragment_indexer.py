import os
import pytesseract
from PIL import Image
from pathlib import Path
import uuid
import json
from datetime import datetime

INPUT_DIR = "C:/real_memory_system/FEEDING_TIME"
OUTPUT_LOG = "logs/media_index_log.jsonl"
CATEGORY = "media"
SUBCATEGORY = "ocr"


def process_image(filepath):
    try:
        img = Image.open(filepath)
        text = pytesseract.image_to_string(img)
        if len(text.strip()) == 0:
            return None
        return text.strip()
    except Exception as e:
        print(f"[SKIP] {filepath}: {e}")
        return None


def index_images():
    for file in Path(INPUT_DIR).rglob("*.png"):
        extract_and_log(file)
    for file in Path(INPUT_DIR).rglob("*.jpg"):
        extract_and_log(file)
    for file in Path(INPUT_DIR).rglob("*.jpeg"):
        extract_and_log(file)


def extract_and_log(path):
    text = process_image(path)
    if not text:
        return

    fragment = {
        "id": str(uuid.uuid4())[:8],
        "claim": text[:100],
        "sub_category": SUBCATEGORY,
        "confidence": 0.9,
        "tags": ["ocr", "image", "indexed"],
        "timestamp": datetime.utcnow().isoformat(),
        "filepath": str(path),
        "content": text
    }

    with open(OUTPUT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(fragment) + "\n")

    print(f"[✔] Indexed {path.name}")


if __name__ == "__main__":
    index_images()
