import os
from pathlib import Path

# Mapping of problematic Unicode -> Safe ASCII equivalents
UNICODE_REPLACEMENTS = {
    'OK': 'OK',
    '->': '->',
    'LAUNCH': 'LAUNCH',
    'TIME': 'TIME',
    'ERROR': 'ERROR',
    'INFO': 'INFO',
    'CONFIG': 'CONFIG',
    '[OK]': '[OK]',
    'WARNING': 'WARNING',
    '>>': '>>',
    'STOP': 'STOP',
}

def sanitize_file(path):
    try:
        original = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[SKIP] Could not read {path}: {e}")
        return

    modified = original
    for uni, safe in UNICODE_REPLACEMENTS.items():
        modified = modified.replace(uni, safe)

    if modified != original:
        path.write_text(modified, encoding="utf-8")
        print(f"[OK] Sanitized: {path}")
    else:
        print(f"[--] Clean: {path}")

def sanitize_folder(folder):
    folder = Path(folder)
    for path in folder.rglob("*.py"):
        sanitize_file(path)

if __name__ == "__main__":
    root = Path(".")  # Current folder
    print("[*] Starting Unicode sanitization...")
    sanitize_folder(root)
    print("[DONE] All .py files sanitized.")
