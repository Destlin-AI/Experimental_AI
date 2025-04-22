
import psutil
import time

def mirror_behavior(threshold=20):
    while True:
        for proc in psutil.process_iter(['name', 'cpu_percent']):
            if proc.info['cpu_percent'] > threshold:
                print(f"👁️ Watching: {proc.info}")
        time.sleep(3)

if __name__ == "__main__":
    mirror_behavior()
