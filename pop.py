import os
import requests
from tqdm import tqdm

# === CONFIG ===
DOWNLOAD_DIR = "massive_datasets"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# === LIST OF DATASETS ===
DATASETS = {
    # --- TEXT ---
    "pile_train": "https://the-eye.eu/public/AI/pile/train.jsonl.zst",
    "pile_val":   "https://the-eye.eu/public/AI/pile/val.jsonl.zst",
    "pile_test":  "https://the-eye.eu/public/AI/pile/test.jsonl.zst",
    "wikipedia_en": "https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2",
    "commoncrawl_sample": "https://data.commoncrawl.org/crawl-data/CC-MAIN-2024-10/segments/1700071270090.54/wet/CC-MAIN-20240318003555-20240318033555-00000.warc.wet.gz",

    # --- IMAGE ---
    "coco_train2017": "http://images.cocodataset.org/zips/train2017.zip",
    "coco_val2017":   "http://images.cocodataset.org/zips/val2017.zip",
    "coco_ann":       "http://images.cocodataset.org/annotations/annotations_trainval2017.zip",
    "openimages_classes": "https://storage.googleapis.com/openimages/2018_04/class-descriptions-boxable.csv",

    # --- AUDIO ---
    "librispeech_dev": "https://www.openslr.org/resources/12/dev-clean.tar.gz",
    "librispeech_test": "https://www.openslr.org/resources/12/test-clean.tar.gz",
    "librispeech_train_100": "https://www.openslr.org/resources/12/train-clean-100.tar.gz",
    "librispeech_train_360": "https://www.openslr.org/resources/12/train-clean-360.tar.gz",
    "librispeech_train_other": "https://www.openslr.org/resources/12/train-other-500.tar.gz",

    # --- VIDEO ---
    "ucf101": "https://www.crcv.ucf.edu/data/UCF101/UCF101.rar",

    # --- BIO / SCI ---
    # GenBank is FTP only — we skip it or handle separately
}

# === DOWNLOAD FUNC ===
def download(url, filename):
    path = os.path.join(DOWNLOAD_DIR, filename)
    try:
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))
            with open(path, 'wb') as f, tqdm(
                total=total,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                desc=filename
            ) as bar:
                for chunk in r.iter_content(1024 * 1024):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))
        print(f"[OK] Downloaded: {filename}")
    except Exception as e:
        print(f"[✗] Failed: {filename}\n    URL: {url}\n    Reason: {e}")

# === GO ===
for name, url in DATASETS.items():
    filename = url.split("/")[-1]
    download(url, filename)

print("\n[OK] All downloads attempted. Check the 'massive_datasets' folder.")
