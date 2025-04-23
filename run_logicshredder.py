from core.config_loader import get
"""
LOGICSHREDDER :: run_logicshredder.py
Unified launcher that respects neuro.lock and intelligently spawns agent swarm
"""

import os
import subprocess
import time
import platform
import threading
from utils import agent_profiler
# [PROFILER_INJECTED]
threading.Thread(target=agent_profiler.run_profile_loop, daemon=True).start()
from pathlib import Path

AGENTS = {
    "token_agent": "agents/token_agent.py",
    "validator": "agents/validator.py",
    "guffifier": "agents/guffifier_v2.py",
    "mutation_engine": "agents/mutation_engine.py",
    "dreamwalker": "agents/dreamwalker.py",
    "meta_agent": "agents/meta_agent.py",
    "cold_logic_mover": "agents/cold_logic_mover.py",
    "cortex_logger": "agents/cortex_logger.py",
}

LOCK_FILE = Path("core/neuro.lock")

def is_locked():
    return LOCK_FILE.exists()

def should_skip(agent_name):
    # Lock disables mutation, walk, dream agents
    locked_agents = ["token_agent", "dreamwalker", "mutation_engine"]
    return agent_name in locked_agents and is_locked()

def launch_agent(agent_name, path):
    if should_skip(agent_name):
        print(f"[run_logicshredder] ⏸ Skipped {agent_name} (brain is locked)")
        return

    interpreter = "python" if platform.system() == "Windows" else "python3"
    try:
        subprocess.Popen([interpreter, path])
        print(f"[run_logicshredder] [OK] Launched: {agent_name}")
    except Exception as e:
        print(f"[run_logicshredder] ERROR Failed to launch {agent_name}: {e}")

def main():
    print("INFO LOGICSHREDDER is activating...")
    if is_locked():
        print("🔒 Brain is LOCKED. Only non-destructive modules will run.")
    else:
        print("🔓 Brain is ACTIVE. Full cognition mode engaged.")

    for agent_name, script_path in AGENTS.items():
        launch_agent(agent_name, script_path)
        time.sleep(0.5)  # Prevent CPU spike at boot

    print("[run_logicshredder] Launch complete. Mind is operational.")

if __name__ == "__main__":
    main()
# [CONFIG_PATCHED]
