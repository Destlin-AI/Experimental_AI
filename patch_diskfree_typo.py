"""
LOGICSHREDDER :: patch_diskfree_typo.py
Purpose: Replace all old 'disk_free' keys with 'disk_free_total' in auto_configurator.py
"""

from pathlib import Path
import shutil

target = Path("auto_configurator.py")
backup = Path("auto_configurator.backup2.py")

if not target.exists():
    print("ERROR auto_configurator.py not found.")
    exit(1)

text = target.read_text(encoding="utf-8")

if "disk_free" not in text:
    print("[OK] No 'disk_free' references left. You're clean.")
    exit(0)

# Make a backup
shutil.copy(target, backup)
print(f"📋 Backup saved as {backup.name}")

# Replace all occurrences
patched = text.replace("disk_free", "disk_free_total")
target.write_text(patched, encoding="utf-8")

print("[OK] All 'disk_free' references replaced with 'disk_free_total'")
print("💉 You are now free of the circular logic hemorrhage.")
