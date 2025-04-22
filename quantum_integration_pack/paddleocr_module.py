
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

img_path = "page_sample.png"
result = ocr.ocr(img_path, cls=True)
for line in result:
    print("🧾 OCR Result:", line)
