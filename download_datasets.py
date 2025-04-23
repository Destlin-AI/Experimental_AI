import os
import sys
import subprocess

# Auto-install required packages
def ensure_package(pkg):
    try:
        __import__(pkg)
    except ImportError:
        print(f"[!] Installing missing package: {pkg}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

for pkg in ['requests', 'tqdm']:
    ensure_package(pkg)

import requests
from tqdm import tqdm

# === CONFIGURATION ===
DOWNLOAD_FOLDER = "datasets"
DATASET_URLS = [
    "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data",
    "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv",
    "https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv"
]

# === CREATE FOLDER ===
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
print(f"[+] Download folder: {os.path.abspath(DOWNLOAD_FOLDER)}")

# === DOWNLOAD FUNCTION ===
def download_file(url):
    local_filename = os.path.join(DOWNLOAD_FOLDER, url.split('/')[-1])
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            with open(local_filename, 'wb') as f:
                with tqdm(
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    desc=local_filename
                ) as bar:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            bar.update(len(chunk))
        print(f"[OK] Saved: {local_filename}")
    except Exception as e:
        print(f"[✗] Failed: {url}\n    Reason: {e}")

# === PROCESS ALL URLS ===
for url in DATASET_URLS:
    download_file(url)
