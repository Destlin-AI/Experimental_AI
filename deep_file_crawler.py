import os
import hashlib
from datetime import datetime

def hash_file(path, chunk_size=8192):
    try:
        hasher = hashlib.md5()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        return f"ERROR: {e}"

def crawl_directory(root_path, out_path):
    count = 0
    with open(out_path, 'w') as out_file:
        for dirpath, dirnames, filenames in os.walk(root_path):
            for file in filenames:
                full_path = os.path.join(dirpath, file)
                try:
                    stat = os.stat(full_path)
                    hashed = hash_file(full_path)
                    line = f"{full_path} | {stat.st_size} bytes | hash: {hashed}"
                except Exception as e:
                    line = f"{full_path} | ERROR: {str(e)}"
                out_file.write(line + "\n")
                count += 1
                if count % 100 == 0:
                    print(f"[+] {count} files crawled...")

    print(f"[OK] Crawl complete. Total files: {count}")
    print(f"[OK] Full output saved to: {out_path}")

if __name__ == "__main__":
    BASE = "."
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_txt = f"neurostore_crawl_output_{timestamp}.txt"
    print(f"[*] Starting deep crawl on: {BASE}")
    crawl_directory(BASE, output_txt)
