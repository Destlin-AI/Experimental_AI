
import pytesseract
from PIL import ImageGrab
import time

def capture_screen():
    img = ImageGrab.grab()
    text = pytesseract.image_to_string(img)
    return text

if __name__ == "__main__":
    while True:
        print("🖥️ OCR Capture:
", capture_screen())
        time.sleep(3)
