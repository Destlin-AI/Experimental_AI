# combine_to_pdf.py
# Converts any supported file (.txt, .md, .py, .pdf, .jpg, .png, etc.) into a PDF

import sys
from pathlib import Path
from fpdf import FPDF
from PyPDF2 import PdfMerger
from PIL import Image

TEXT_EXTS = {'.txt', '.md', '.py'}
IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}
PDF_EXT = '.pdf'

def convert_text_to_pdf(txt_path, output_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Courier", size=10)
    with open(txt_path, "r", encoding="utf-8") as f:
        for line in f:
            pdf.multi_cell(0, 10, line.strip())
    pdf.output(output_path)

def convert_image_to_pdf(img_path, output_path):
    image = Image.open(img_path).convert("RGB")
    image.save(output_path)

def convert_to_pdf(file_path):
    path = Path(file_path)
    ext = path.suffix.lower()
    output_path = path.with_suffix('.pdf')

    if ext in TEXT_EXTS:
        convert_text_to_pdf(path, output_path)
    elif ext in IMAGE_EXTS:
        convert_image_to_pdf(path, output_path)
    elif ext == PDF_EXT:
        return path  # Already PDF
    else:
        raise Exception(f"Unsupported format: {file_path}")
    
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python combine_to_pdf.py file1 [file2 ...]")
        sys.exit(1)

    for file in sys.argv[1:]:
        try:
            pdf_path = convert_to_pdf(file)
            print(f"[✓] Converted: {file} -> {pdf_path}")
        except Exception as e:
            print(f"[✗] {file} failed: {e}")


