
import threading
import time
import socket
import psutil

TEMP_THRESHOLD = 65  # Celsius

def broadcast_swarm_alert():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    msg = b"SWARM_ALERT: Thermal throttle triggered"
    sock.sendto(msg, ('<broadcast>', 9999))

def monitor_temp():
    while True:
        temps = psutil.sensors_temperatures()
        if "coretemp" in temps:
            core_temp = temps["coretemp"][0].current
            print(f"🌡️ Core Temp: {core_temp}")
            if core_temp > TEMP_THRESHOLD:
                print("🚨 Alert: Throttling swarm")
                broadcast_swarm_alert()
                time.sleep(10)
        time.sleep(3)

if __name__ == "__main__":
    threading.Thread(target=monitor_temp).start()
