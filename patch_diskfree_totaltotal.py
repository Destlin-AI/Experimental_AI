"""
LOGICSHREDDER :: patch_diskfree_totaltotal.py
Purpose: Fix accidental 'disk_free_total_total' typo in auto_configurator.py
"""

from pathlib import Path
import shutil

target = Path("auto_configurator.py")
backup = Path("auto_configurator.repaired.py")

if not target.exists():
    print("ERROR auto_configurator.py not found.")
    exit(1)

code = target.read_text(encoding="utf-8")

if "disk_free_total_total" not in code:
    print("[OK] No 'disk_free_total_total' found. Already clean.")
    exit(0)

shutil.copy(target, backup)
print(f"📋 Backup saved as {backup.name}")

# FIX THE TYPED ABOMINATION
patched = code.replace("disk_free_total_total", "disk_free_total")
target.write_text(patched, encoding="utf-8")

print("[OK] Fixed: 'disk_free_total_total' -> 'disk_free_total'")
print("💉 Logic has been purified. Run the boot again.")
