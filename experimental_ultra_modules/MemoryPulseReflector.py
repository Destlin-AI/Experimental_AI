
import psutil
import time

def pulse_reflector():
    while True:
        usage = psutil.virtual_memory().percent
        print(f"🧠 RAM Pulse: {usage}%")
        time.sleep(3)

if __name__ == "__main__":
    pulse_reflector()
