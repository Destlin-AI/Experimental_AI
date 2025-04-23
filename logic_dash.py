"""
LOGICSHREDDER :: logic_dash.py (Part 1/2)
Purpose: Live terminal dashboard showing system status and cognitive state
"""

import curses
import time
import os
import yaml
from pathlib import Path
import psutil
from core.config_loader import get

HEATMAP = Path("logs/logic_heatmap.yaml")
LOCK_FILE = Path("core/neuro.lock")
SNAPSHOT_DIR = Path("snapshots/")
AGENT_STATS = Path("logs/agent_stats/")

REFRESH_INTERVAL = 5

def get_hot_beliefs(n=5):
    if not HEATMAP.exists():
        return []
    try:
        data = yaml.safe_load(open(HEATMAP, 'r', encoding='utf-8'))
        sorted_data = sorted(data.items(), key=lambda x: x[1].get("heat_score", 0), reverse=True)
        return sorted_data[:n]
    except Exception as e:
        return [("error_loading", {"heat_score": 0.0})]

def get_lock_status():
    return LOCK_FILE.exists()

def get_last_snapshot_time():
    if not SNAPSHOT_DIR.exists():
        return "Never"
    files = list(SNAPSHOT_DIR.glob("*.tar.gz"))
    if not files:
        return "Never"
    latest = max(files, key=os.path.getctime)
    age = int(time.time() - os.path.getctime(latest))
    minutes = age // 60
    return f"{minutes}m ago"

def get_agent_usage():
    stats = []
    for file in AGENT_STATS.glob("*.stat"):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if not lines:
                    continue
                last = lines[-1].strip().split(",")
                stats.append({
                    "name": file.stem,
                    "cpu": float(last[1]),
                    "mem": float(last[2]),
                    "read": float(last[3]),
                    "write": float(last[4])
                })
        except:
            continue
    return stats

def draw_static(stdscr):
    stdscr.clear()
    stdscr.border()
    stdscr.addstr(1, 2, "LOGICSHREDDER: REAL-TIME DASH", curses.A_BOLD)
    stdscr.addstr(3, 4, "AGENTS STATUS", curses.A_UNDERLINE)
    stdscr.addstr(3, 35, "RESOURCE USAGE", curses.A_UNDERLINE)
    stdscr.addstr(10, 4, "🔥 HOT BELIEFS (TOP 5)", curses.A_UNDERLINE)
    stdscr.addstr(18, 4, "[Q] Quit  |  [L] Lock Brain  |  [U] Unlock Brain", curses.A_DIM)
def draw_dynamic(stdscr):
    lock_status = "LOCKED" if get_lock_status() else "UNLOCKED"
    snap_time = get_last_snapshot_time()
    agents = get_agent_usage()
    beliefs = get_hot_beliefs()

    for i, agent in enumerate(agents[:6]):
        stdscr.addstr(4 + i, 4, f"{agent['name']:<16} [OK]")
        stdscr.addstr(4 + i, 35, f"CPU: {agent['cpu']}% | MEM: {agent['mem']} MB")

    stdscr.addstr(4, 65, f"I/O:")
    stdscr.addstr(5, 65, f"Read: {sum(a['read'] for a in agents):.1f} MB")
    stdscr.addstr(6, 65, f"Write: {sum(a['write'] for a in agents):.1f} MB")
    stdscr.addstr(7, 65, f"Last snapshot: {snap_time}")
    stdscr.addstr(8, 65, f"Lock status: {lock_status}")

    for i, (fid, data) in enumerate(beliefs):
        claim = fid.replace("frag_", "")[:16]
        score = data.get("heat_score", 0.0)
        stdscr.addstr(11 + i, 6, f"- {claim:<18} (heat: {score:.2f})")

def toggle_lock(lock=True):
    if lock:
        Path("core/neuro.lock").write_text(str(int(time.time())))
    else:
        Path("core/neuro.lock").unlink(missing_ok=True)

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    while True:
        draw_static(stdscr)
        draw_dynamic(stdscr)
        stdscr.refresh()
        for _ in range(REFRESH_INTERVAL * 10):
            key = stdscr.getch()
            if key == ord("q"):
                return
            elif key == ord("l"):
                toggle_lock(True)
            elif key == ord("u"):
                toggle_lock(False)
            time.sleep(0.1)

if __name__ == "__main__":
    curses.wrapper(main)
