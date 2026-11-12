import io
import fitz
import base64
import zipfile
from App import app

def test_reordered_downloads():
    client = app.test_client()

    # Create dummy images (Red page 1, Blue page 2, Green page 3)
    def create_dummy_b64_img(color):
        doc = fitz.open()
        p = doc.new_page(width=100, height=100)
        p.draw_rect(fitz.Rect(0, 0, 100, 100), fill=color)
        pix = p.get_pixmap()
        img_bytes = pix.tobytes("jpeg")
        doc.close()
        return f"data:image/jpeg;base64,{base64.b64encode(img_bytes).decode('utf-8')}"

    img1 = create_dummy_b64_img((1, 0, 0)) # Red (Page 1 original)
    img2 = create_dummy_b64_img((0, 1, 0)) # Green (Page 2 original)
    img3 = create_dummy_b64_img((0, 0, 1)) # Blue (Page 3 original)

    # Reordered pages list: [img3 (Blue), img1 (Red), img2 (Green)]
    reordered_pages = [
        {'data_url': img3, 'page': 1, 'pageNumber': 1},
        {'data_url': img1, 'page': 2, 'pageNumber': 2},
        {'data_url': img2, 'page': 3, 'pageNumber': 3}
    ]

    # 1. Test ZIP Download with Drag & Drop reordered pages
    res_zip = client.post('/download_pdf_zip', json={
        'pages': reordered_pages,
        'pdf_name': 'test_reordered'
    })
    assert res_zip.status_code == 200, f"ZIP download failed: {res_zip.status_code}"
    
    zip_bytes = res_zip.data
    zip_file = zipfile.ZipFile(io.BytesIO(zip_bytes))
    namelist = zip_file.namelist()
    assert len(namelist) == 3, f"Expected 3 files in zip, got {len(namelist)}"
    assert namelist == ['page_1.jpg', 'page_2.jpg', 'page_3.jpg'], f"ZIP filenames unexpected: {namelist}"
    print("Reordered ZIP download test PASSED!")

    # 2. Test PDF Download with Drag & Drop reordered pages
    res_pdf = client.post('/download_pdf_file', json={
        'pages': reordered_pages,
        'file_name': 'test_reordered_pdf'
    })
    assert res_pdf.status_code == 200, f"PDF download failed: {res_pdf.status_code}"
    
    pdf_bytes = res_pdf.data
    doc_out = fitz.open(stream=pdf_bytes, filetype="pdf")
    assert len(doc_out) == 3, f"Expected 3 pages in reordered PDF, got {len(doc_out)}"
    doc_out.close()
    print("Reordered PDF download test PASSED!")

    print("\nALL REORDERED DRAG & DROP DOWNLOAD TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    test_reordered_downloads()
