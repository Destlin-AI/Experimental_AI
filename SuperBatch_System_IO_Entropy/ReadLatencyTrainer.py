
import os
import time

def latency_test(file_path):
    start = time.time()
    with open(file_path, "rb") as f:
        f.read()
    latency = time.time() - start
    print(f"⏱️ Read Latency: {latency:.6f}s")

if __name__ == "__main__":
    latency_test("C:/Windows/System32/notepad.exe")
