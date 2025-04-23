from core.config_loader import get
"""
LOGICSHREDDER :: cortex_bus.py
Purpose: Handle agent communication via in-memory queue + SQLite fallback
"""

import sqlite3
import threading
import time
import os
import threading
from utils import agent_profiler
# [PROFILER_INJECTED]
threading.Thread(target=agent_profiler.run_profile_loop, daemon=True).start()
from queue import Queue

DB_PATH = "core/cortex_memory.db"
os.makedirs("core", exist_ok=True)

# Message Queue
message_queue = Queue()

# SQLite Initialization
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            type TEXT,
            payload TEXT,
            timestamp INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Write to SQLite
def persist_message(msg):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO messages (sender, type, payload, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (
            msg.get('from', 'unknown'),
            msg.get('type', 'generic'),
            str(msg.get('payload')),
            int(msg.get('timestamp', time.time()))
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[cortex_bus] Failed to persist message: {e}")

# Ingest message from any agent
def send_message(msg):
    message_queue.put(msg)
    persist_message(msg)

# Message Dispatcher (for future extensions)
def process_messages():
    while True:
        if not message_queue.empty():
            msg = message_queue.get()
            # This is where you'd route the message to a handler or hook system
            print(f"[cortex_bus] Routed: {msg.get('type')} from {msg.get('from')}")
        time.sleep(0.05)

# Optional background thread runner
def start_dispatcher():
    dispatcher = threading.Thread(target=process_messages, daemon=True)
    dispatcher.start()

if __name__ == "__main__":
    print("[cortex_bus] Starting dispatcher...")
    start_dispatcher()
    while True:
        time.sleep(1)
# [CONFIG_PATCHED]
