
import os
import hashlib
import time

def bond_pid(pid):
    entropy = f"{pid}-{time.time()}".encode()
    bind = hashlib.sha256(entropy).hexdigest()
    print(f"🔗 Bonded PID {pid} to entropy hash {bind}")

if __name__ == "__main__":
    bond_pid(os.getpid())
