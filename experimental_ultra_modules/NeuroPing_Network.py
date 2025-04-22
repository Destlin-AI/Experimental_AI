
import socket
import threading
import time

def pulse(ip="255.255.255.255", port=48888, msg=b"NEUROPING"):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        sock.sendto(msg, (ip, port))
        print("🧠 Pulse sent.")
        time.sleep(2)

def listen(port=48888):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", port))
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"🧠 Received from {addr}: {data}")

if __name__ == "__main__":
    threading.Thread(target=listen, daemon=True).start()
    pulse()
