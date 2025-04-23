import os
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# Define classification rules
FILE_MAP = {
    'data': [".csv", "train_", "test_", "repeat-config", "NCI-config"],
    'models': [".pt", ".pkl", ".gguf"],
    'fragments': [".yaml"],
    'logs': [".log", "mutation_log", "contradictions"],
    'runtime': ["vm_states", "snapshots"],
    'meta': ["audit_", "system_config", "optimized_paths"],
    'agents': [
        "validator.py", "dreamwalker.py", "quant_prompt_feeder.py",
        "run_logicshredder.py", "subcon_layer_mapper.py"
    ],
    'scripts': ["backup", "setup", "install", "crawler"],
    'media': [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"],
    'ui': [".html", ".css", ".js", ".mjs", "favicon"],
    'docs': ["readme", "README", ".md"],
    'ci': ["pytest", "tests.sh", "conftest.py"],
}

LOG_FILE = Path("logs/file_sage_log.txt")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def classify_file(file):
    name = file.name.lower()
    for folder, patterns in FILE_MAP.items():
        for pattern in patterns:
            if pattern in name:
                return folder
    if file.suffix == ".py":
        return "scripts"  # fallback for miscellaneous .py files
    return None


def move_file(file, target_folder, dry_run=False):
    target_path = Path(target_folder)
    target_path.mkdir(parents=True, exist_ok=True)
    new_loc = target_path / file.name

    if not dry_run:
        shutil.move(str(file), str(new_loc))

    with open(LOG_FILE, 'a', encoding='utf-8') as log:
        log.write(f"[{datetime.now()}] Moved '{file}' -> '{new_loc}'\n")
    print(f"[✓] Moved '{file.name}' -> {target_folder}/")


def scan_and_sort(root, dry_run=False):
    all_files = [p for p in Path(root).rglob("*") if p.is_file() and not p.name.startswith(".")]
    for file in all_files:
        folder = classify_file(file)
        if folder:
            move_file(file, folder, dry_run=dry_run)
        else:
            print(f"[~] Unknown file: {file.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true", help="Run in dry mode (no file moves)")
    args = parser.parse_args()

    print("\n🧠 FILE SAGE INITIATED\n============================\n")
    scan_and_sort(".", dry_run=args.preview)
    print("\n[✓] File classification complete.\n")
