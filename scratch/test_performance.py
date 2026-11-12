import time
import io
import fitz
from PIL import Image
import pandas as pd
from docx import Document

from App import convert_any_file_to_jpg, convert_any_file_to_pdf, process_fitz_doc, process_pillow_image

def benchmark():
    # 1. Create a dummy multi-page PDF with 20 pages
    pdf_doc = fitz.open()
    for i in range(20):
        page = pdf_doc.new_page(width=595, height=842)
        page.insert_text((50, 50), f"This is test page {i+1}", fontsize=20)
        page.draw_rect(fitz.Rect(100, 100, 400, 400), color=(1, 0, 0), fill=(0.8, 0.9, 1))
    pdf_bytes = pdf_doc.tobytes()
    pdf_doc.close()

    print(f"Generated test PDF of size: {len(pdf_bytes)} bytes (20 pages)")

    # Test PDF to JPG speed
    t0 = time.time()
    pages_data, zip_b64 = convert_any_file_to_jpg(pdf_bytes, "test.pdf", dpi=300)
    t1 = time.time()
    print(f"PDF to JPG (300 DPI, 20 pages): {t1 - t0:.3f} seconds")

    t0 = time.time()
    pages_data_150, zip_b64_150 = convert_any_file_to_jpg(pdf_bytes, "test.pdf", dpi=150)
    t1 = time.time()
    print(f"PDF to JPG (150 DPI, 20 pages): {t1 - t0:.3f} seconds")

    # Test PDF to PDF preview generation speed
    t0 = time.time()
    pdf_out = convert_any_file_to_pdf(pdf_bytes, "test.pdf")
    t1 = time.time()
    print(f"PDF to PDF conversion: {t1 - t0:.3f} seconds")

    # Create dummy docx
    doc = Document()
    for i in range(10):
        doc.add_heading(f"Section {i+1}", level=1)
        doc.add_paragraph("This is a test paragraph for docx conversion speed test.")
        table = doc.add_table(rows=3, cols=3)
        for r in range(3):
            for c in range(3):
                table.cell(r, c).text = f"Cell {r},{c}"
    docx_buf = io.BytesIO()
    doc.save(docx_buf)
    docx_bytes = docx_buf.getvalue()

    t0 = time.time()
    pages_data_docx, _ = convert_any_file_to_jpg(docx_bytes, "test.docx", dpi=150)
    t1 = time.time()
    print(f"DOCX to JPG (150 DPI): {t1 - t0:.3f} seconds")

if __name__ == '__main__':
    benchmark()
