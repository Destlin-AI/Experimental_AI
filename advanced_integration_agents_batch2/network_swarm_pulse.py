
import socket
import time

def broadcast_pulse(port=9999):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = b"🐜 Swarm Ping"
    while True:
        sock.sendto(message, ('<broadcast>', port))
        print("📡 Pulse sent")
        time.sleep(5)

if __name__ == "__main__":
    broadcast_pulse()
