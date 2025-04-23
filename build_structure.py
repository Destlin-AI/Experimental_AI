"""
LOGICSHREDDER :: build_structure.py
Purpose: Create the full file/folder structure for the LOGICSHREDDER project
"""

from pathlib import Path

BASE = Path(".")  # run from root folder like: python build_structure.py

DIRS = [
    "agents",
    "core",
    "fragments/core",
    "fragments/incoming",
    "fragments/archive",
    "fragments/overflow",
    "fragments/cold",
    "input",
    "logs",
    "logs/agent_stats",
    "quant/models",
    "snapshots",
    "configs",
    "utils"
]

FILES = [
    "run_logicshredder.py",
    "neuro_lock.py",
    "start_logicshredder.bat",
    "start_logicshredder_silent.bat",
    "inject_profiler.py",
    "build_structure.py"
]

def make_dirs():
    for d in DIRS:
        path = BASE / d
        path.mkdir(parents=True, exist_ok=True)
        keep = path / ".gitkeep"
        keep.touch()
        print(f"[structure] 📁 Created: {d}/")

def make_files():
    for f in FILES:
        path = BASE / f
        if not path.exists():
            path.write_text("# Auto-created placeholder\n")
            print(f"[structure] 📄 Created placeholder: {f}")

if __name__ == "__main__":
    print("CONFIG Building LOGICSHREDDER file structure...")
    make_dirs()
    make_files()
    print("[OK] Project structure initialized.")
