
import psutil
import time

def monitor_and_throttle(threshold=65):
    while True:
        temps = psutil.sensors_temperatures()
        if "coretemp" in temps:
            core_temp = temps["coretemp"][0].current
            print(f"🌡️ CPU Temp: {core_temp}")
            if core_temp > threshold:
                print("🚨 Throttling AI threads!")
                time.sleep(5)
        time.sleep(2)

if __name__ == "__main__":
    monitor_and_throttle()
