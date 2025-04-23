from PyPDF2 import PdfReader, PdfWriter
import os

def shrink_pdf(input_path, output_path):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)

if __name__ == "__main__":
    input_pdf = "symbolic_manifesto-compressed-merged-compressed.pdf"
    output_pdf = "symbolic_manifesto-shrunk-lossless.pdf"
    
    if os.path.exists(input_pdf):
        shrink_pdf(input_pdf, output_pdf)
        print(f"[✓] Saved: {output_pdf}")
    else:
        print("[✗] Input PDF not found.")
