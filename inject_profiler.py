from core.config_loader import get
"""
LOGICSHREDDER :: inject_profiler.py (Windows Staging Edition)
Purpose: Inject agent_profiler code into all real agents inside Allinonepy\agents\
"""

import threading
from pathlib import Path

# Your specific folder path (Windows safe)
AGENTS_DIR = Path("C:/Users/PC/Desktop/Operation Future/Allinonepy/agents")
PROFILER_IMPORT = "from utils import agent_profiler"
PROFILER_BOOT = "threading.Thread(target=agent_profiler.run_profile_loop, daemon=True).start()"
INJECTION_TAG = "# [PROFILER_INJECTED]"

def already_injected(code):
    return INJECTION_TAG in code or "agent_profiler" in code

def inject_profiler_code(file_path):
    try:
        code = file_path.read_text(encoding='utf-8')

        if already_injected(code):
            print(f"[inject_profiler] Skipped (already injected): {file_path.name}")
            return

        lines = code.splitlines()
        new_lines = []
        inserted = False

        for i, line in enumerate(lines):
            new_lines.append(line)
            if not inserted and line.strip().startswith("import"):
                if i + 1 < len(lines) and not lines[i + 1].startswith("import"):
                    new_lines.append("import threading")
                    new_lines.append(PROFILER_IMPORT)
                    new_lines.append(INJECTION_TAG)
                    new_lines.append(PROFILER_BOOT)
                    inserted = True

        if inserted:
            file_path.write_text("\n".join(new_lines), encoding='utf-8')
            print(f"[inject_profiler] [OK] Injected into: {file_path.name}")
        else:
            print(f"[inject_profiler] WARNING Could not inject into: {file_path.name}")

    except Exception as e:
        print(f"[inject_profiler] ERROR Error with {file_path.name}: {e}")

def main():
    if not AGENTS_DIR.exists():
        print(f"[inject_profiler] ERROR: Cannot find directory: {AGENTS_DIR}")
        return

    for py_file in AGENTS_DIR.glob("*.py"):
        inject_profiler_code(py_file)

if __name__ == "__main__":
    main()

# [CONFIG_PATCHED]
