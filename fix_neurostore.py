import os
import zipfile
from pathlib import Path

def write_file(path_parts, content):
    path = Path(*path_parts)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"[OK] Fixed or created: {path}")

def fix_zip_project():
    zip_code = '''
import zipfile
from pathlib import Path

def zip_project():
    BASE = Path(".")
    zip_path = BASE.with_suffix(".zip")
    print(f"\\n[OK] Zipping project to: {zip_path}")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in BASE.rglob("*"):
            if file.is_file():
                zipf.write(file, arcname=file.relative_to(BASE))
    print("[OK] ZIP complete.")

if __name__ == "__main__":
    zip_project()
'''
    write_file(["zip_project.py"], zip_code)

def fix_inject_profiler():
    inject_code = '''
import time
import psutil

class InjectProfiler:
    def __init__(self, label="logic_injection"):
        self.label = label
        self.snapshots = []

    def snapshot(self):
        mem = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent(interval=0.1)
        self.snapshots.append((time.time(), mem, cpu))

    def report(self):
        print(f"[Profiler:{self.label}] Total snapshots: {len(self.snapshots)}")
        for t, mem, cpu in self.snapshots:
            print(f" - {round(t, 2)}s :: MEM {mem}% | CPU {cpu}%")

if __name__ == "__main__":
    p = InjectProfiler()
    for _ in range(5):
        p.snapshot()
        time.sleep(1)
    p.report()
'''
    write_file(["inject_profiler.py"], inject_code)

def main():
    print("[🛠] Repairing NeuroStore core...")
    fix_zip_project()
    fix_inject_profiler()
    print("[OK] Repair complete. Ready to run.")

if __name__ == "__main__":
    main()
