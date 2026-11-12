import time
import fitz
import io
import base64
import zipfile
import os
from concurrent.futures import ThreadPoolExecutor

def process_fitz_fast(doc, dpi=150, quality=85):
    total_pages = len(doc)
    
    def render_page(i):
        page = doc.load_page(i)
        pix = page.get_pixmap(dpi=dpi, alpha=False)
        img_bytes = pix.tobytes("jpeg", jpg_quality=quality)
        img_filename = f"page_{i + 1}.jpg"
        b64_str = base64.b64encode(img_bytes).decode('utf-8')
        return i, img_filename, img_bytes, {
            'page': i + 1,
            'filename': img_filename,
            'data_url': f"data:image/jpeg;base64,{b64_str}",
            'width': pix.width,
            'height': pix.height
        }

    with ThreadPoolExecutor(max_workers=min(16, (os.cpu_count() or 4) * 2)) as executor:
        rendered = list(executor.map(render_page, range(total_pages)))

    rendered.sort(key=lambda x: x[0])

    pages_data = []
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_STORED) as zip_file:
        for _, img_filename, img_bytes, page_dict in rendered:
            zip_file.writestr(img_filename, img_bytes)
            pages_data.append(page_dict)

    doc.close()
    zip_buffer.seek(0)
    zip_b64 = base64.b64encode(zip_buffer.getvalue()).decode('utf-8')
    return pages_data, zip_b64

def test_fitz():
    pdf_doc = fitz.open()
    for i in range(20):
        page = pdf_doc.new_page(width=595, height=842)
        page.insert_text((50, 50), f"This is test page {i+1}", fontsize=20)
        page.draw_rect(fitz.Rect(100, 100, 400, 400), color=(1, 0, 0), fill=(0.8, 0.9, 1))
    
    pdf_bytes = pdf_doc.tobytes()
    pdf_doc.close()

    t0 = time.time()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages_data, zip_b64 = process_fitz_fast(doc, dpi=150, quality=85)
    t1 = time.time()
    print(f"Fast PyMuPDF Threaded PDF to JPG (150 DPI, 20 pages): {t1 - t0:.3f} seconds")

    doc2 = fitz.open(stream=pdf_bytes, filetype="pdf")
    t0 = time.time()
    pages_data_300, _ = process_fitz_fast(doc2, dpi=300, quality=85)
    t1 = time.time()
    print(f"Fast PyMuPDF Threaded PDF to JPG (300 DPI, 20 pages): {t1 - t0:.3f} seconds")

if __name__ == '__main__':
    test_fitz()
