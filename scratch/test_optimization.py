import time
import io
import os
import fitz
import base64
import zipfile
from PIL import Image
import pandas as pd
from docx import Document
from concurrent.futures import ThreadPoolExecutor
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Number of worker threads for parallel page processing
MAX_WORKERS = min(16, (os.cpu_count() or 4) * 2)

def process_fitz_doc_parallel(doc_bytes, filetype="pdf", dpi=150, quality=85):
    # Opening doc in memory per thread or opening document
    doc = fitz.open(stream=doc_bytes, filetype=filetype)
    total_pages = len(doc)

    def render_page(i):
        # Create a fresh thread-safe page object or doc slice
        # PyMuPDF doc.load_page is fast; for thread safety, open thread-local doc if needed or load page
        page_doc = fitz.open(stream=doc_bytes, filetype=filetype)
        page = page_doc.load_page(i)
        pix = page.get_pixmap(dpi=dpi, alpha=False)
        img_bytes = pix.tobytes("jpeg", jpg_quality=quality)
        page_doc.close()

        img_filename = f"page_{i + 1}.jpg"
        b64_str = base64.b64encode(img_bytes).decode('utf-8')
        
        return i, img_filename, img_bytes, {
            'page': i + 1,
            'filename': img_filename,
            'data_url': f"data:image/jpeg;base64,{b64_str}",
            'width': pix.width,
            'height': pix.height
        }

    pages_data = [None] * total_pages
    file_bytes_map = {}

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = executor.map(render_page, range(total_pages))
        for i, img_filename, img_bytes, page_dict in results:
            pages_data[i] = page_dict
            file_bytes_map[img_filename] = img_bytes

    doc.close()

    # Create ZIP buffer using ZIP_STORED (fastest for JPEGs)
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_STORED) as zip_file:
        for filename, bdata in file_bytes_map.items():
            zip_file.writestr(filename, bdata)

    zip_buffer.seek(0)
    zip_b64 = base64.b64encode(zip_buffer.getvalue()).decode('utf-8')
    return pages_data, zip_b64

def test_opt_benchmark():
    # 1. Create a dummy multi-page PDF with 20 pages
    pdf_doc = fitz.open()
    for i in range(20):
        page = pdf_doc.new_page(width=595, height=842)
        page.insert_text((50, 50), f"This is test page {i+1}", fontsize=20)
        page.draw_rect(fitz.Rect(100, 100, 400, 400), color=(1, 0, 0), fill=(0.8, 0.9, 1))
    pdf_bytes = pdf_doc.tobytes()
    pdf_doc.close()

    print("--- Optimized Parallel Benchmark ---")
    
    t0 = time.time()
    pages_data_300, zip_b64_300 = process_fitz_doc_parallel(pdf_bytes, filetype="pdf", dpi=300, quality=85)
    t1 = time.time()
    print(f"Parallel PDF to JPG (300 DPI, 20 pages): {t1 - t0:.3f} seconds")

    t0 = time.time()
    pages_data_150, zip_b64_150 = process_fitz_doc_parallel(pdf_bytes, filetype="pdf", dpi=150, quality=85)
    t1 = time.time()
    print(f"Parallel PDF to JPG (150 DPI, 20 pages): {t1 - t0:.3f} seconds")

if __name__ == '__main__':
    test_opt_benchmark()
