# === MODULE: GUIWrapperLaunch ===

from pathlib import Path
from subprocess import Popen

class GUIWrapperLaunch:
    def __init__(self, base_dir='D:/Project_AI/gui'):
        self.base = Path(base_dir)
        self.backend = self.base / 'manage.py'

    def launch(self):
        if not self.backend.exists():
            print("[❌] Django backend not found.")
            return
        print("[🌐] Launching Symbolic AI GUI Dashboard...")
        Popen(["python", str(self.backend), "runserver", "127.0.0.1:8000"])

# Usage:
# wrapper = GUIWrapperLaunch()
# wrapper.launch()
