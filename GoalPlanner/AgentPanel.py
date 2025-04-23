import os
from pathlib import Path

AGENT_DIR = Path("C:/real_memory_system/scripts")

def list_agents():
    if not AGENT_DIR.exists():
        return {"error": "Agent folder not found."}

    agents = []
    for f in AGENT_DIR.glob("*.py"):
        agents.append(f.name)
    return {"agents": agents}

if __name__ == "__main__":
    print(list_agents())
