# patch_symbolic_emitters.py
import os
from pathlib import Path

PATCHES = {
    "validator.py": {
        "inject": "import redis\nr = redis.Redis(decode_responses=True)\n",
        "target": "send_message({",
        "payload": "r.publish(\"contradiction_found\", payload['claim_1'])  # [AUTO_EMIT]"
    },
    "mutation_engine.py": {
        "inject": "import redis\nr = redis.Redis(decode_responses=True)\n",
        "target": "send_message({",
        "payload": "r.publish(\"decay_event\", new_frag['claim'])  # [AUTO_EMIT]"
    },
    "dreamwalker.py": {
        "inject": "import redis\nr = redis.Redis(decode_responses=True)\n",
        "target": "send_message({",
        "payload": "if frag.get('confidence', 1.0) < 0.4 and depth > 5:\n    r.publish(\"symbolic_alert\", frag['claim'])  # [AUTO_EMIT]"
    }
}

def patch_file(filename, inject_code, hook_line, emit_line):
    path = Path(filename)
    if not path.exists():
        print(f"[!] Skipped missing file: {filename}")
        return

    lines = path.read_text(encoding="utf-8").splitlines()
    modified = []
    injected = False
    hooked = False

    for line in lines:
        if not injected and "import" in line and "yaml" in line:
            modified.append(line)
            modified.append(inject_code)
            injected = True
        elif not hooked and hook_line in line:
            modified.append(emit_line)
            modified.append(line)
            hooked = True
        else:
            modified.append(line)

    path.write_text("\n".join(modified), encoding="utf-8")
    print(f"[✓] Patched {filename}")

if __name__ == "__main__":
    for file, cfg in PATCHES.items():
        patch_file(file, cfg["inject"], cfg["target"], cfg["payload"])
