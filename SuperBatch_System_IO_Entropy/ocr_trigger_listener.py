
import socket
import pytesseract
from PIL import ImageGrab
import time

def capture_screen_text():
    img = ImageGrab.grab()
    return pytesseract.image_to_string(img)

def listen_for_trigger(port=9999):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", port))
    print("🧠 OCR Trigger listener started.")
    while True:
        data, addr = sock.recvfrom(1024)
        if b"SWARM_ALERT" in data:
            print("⚡ OCR triggered by thermal alert.")
            print(capture_screen_text())

if __name__ == "__main__":
    listen_for_trigger()
