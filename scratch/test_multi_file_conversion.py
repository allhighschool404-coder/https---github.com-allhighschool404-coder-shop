import io, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from App import app
from PIL import Image

def test_multi_file_conversions():
    client = app.test_client()

    # Create 2 sample images and 1 text file
    img1 = Image.new('RGB', (100, 100), color='red')
    buf1 = io.BytesIO()
    img1.save(buf1, format='PNG')
    buf1.seek(0)

    img2 = Image.new('RGB', (150, 150), color='green')
    buf2 = io.BytesIO()
    img2.save(buf2, format='JPEG')
    buf2.seek(0)

    txt_buf = io.BytesIO(b"Hello World from test file")

    print("--- 1. Testing Multiple File Upload to JPG (/convert_file) ---")
    data_jpg = {
        'pdf_file': [
            (buf1, 'image1.png'),
            (buf2, 'image2.jpg'),
            (txt_buf, 'doc1.txt')
        ],
        'dpi': '300'
    }
    res_jpg = client.post('/convert_file', data=data_jpg, content_type='multipart/form-data')
    json_jpg = res_jpg.get_json()
    assert res_jpg.status_code == 200, f"Failed: {json_jpg}"
    assert json_jpg['success'] == True
    assert json_jpg['total_files'] == 3
    assert json_jpg['total_pages'] >= 3
    assert 'zip_b64' in json_jpg and len(json_jpg['zip_b64']) > 0
    print(f"Multi JPG Success! Uploaded: 3 files, Total Generated Images: {json_jpg['total_pages']}")

    # Re-create fresh BytesIO buffers for the second test
    buf1_b = io.BytesIO()
    img1.save(buf1_b, format='PNG')
    buf1_b.seek(0)

    buf2_b = io.BytesIO()
    img2.save(buf2_b, format='JPEG')
    buf2_b.seek(0)

    txt_buf_b = io.BytesIO(b"Hello World from test file")

    print("\n--- 2. Testing Multiple File Upload to PDF (/convert_to_pdf) ---")
    data_pdf = {
        'file': [
            (buf1_b, 'image1.png'),
            (buf2_b, 'image2.jpg'),
            (txt_buf_b, 'doc1.txt')
        ]
    }
    res_pdf = client.post('/convert_to_pdf', data=data_pdf, content_type='multipart/form-data')
    json_pdf = res_pdf.get_json()
    assert res_pdf.status_code == 200, f"Failed: {json_pdf}"
    assert json_pdf['success'] == True
    assert json_pdf['total_files'] == 3
    assert json_pdf['total_pages'] >= 3
    assert 'pdf_b64' in json_pdf and len(json_pdf['pdf_b64']) > 0
    print(f"Multi PDF Success! Uploaded: 3 files, Total PDF Pages: {json_pdf['total_pages']}, PDF Size: {json_pdf['pdf_size']} bytes")

    print("\nALL MULTI-FILE CONVERSION TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    test_multi_file_conversions()
