import io, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from App import app, SUPPORTED_EXTENSIONS
from PIL import Image

def test_pdf_converter_routes():
    client = app.test_client()

    # 1. PNG to PDF
    print("Testing PNG to PDF conversion route...")
    img = Image.new('RGB', (200, 200), color='blue')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    res = client.post('/convert_to_pdf', data={'file': (buf, 'test_image.png')}, content_type='multipart/form-data')
    json_data = res.get_json()
    assert res.status_code == 200 and json_data.get('success'), f"PNG to PDF failed: {json_data}"
    print(f"PNG to PDF success! Total pages: {json_data['total_pages']}, PDF size: {json_data['pdf_size']} bytes")

    # 2. SVG to PDF
    print("Testing SVG to PDF conversion route...")
    svg_buf = io.BytesIO(b"<svg width='100' height='100'><rect width='100' height='100' fill='purple'/></svg>")
    res = client.post('/convert_to_pdf', data={'file': (svg_buf, 'test_graphic.svg')}, content_type='multipart/form-data')
    json_data = res.get_json()
    assert res.status_code == 200 and json_data.get('success'), f"SVG to PDF failed: {json_data}"
    print(f"SVG to PDF success! Total pages: {json_data['total_pages']}, PDF size: {json_data['pdf_size']} bytes")

    # 3. TXT to PDF
    print("Testing TXT to PDF conversion route...")
    txt_buf = io.BytesIO(b"Sample document text for PDF creation test.")
    res = client.post('/convert_to_pdf', data={'file': (txt_buf, 'test_text.txt')}, content_type='multipart/form-data')
    json_data = res.get_json()
    assert res.status_code == 200 and json_data.get('success'), f"TXT to PDF failed: {json_data}"
    print(f"TXT to PDF success! Total pages: {json_data['total_pages']}, PDF size: {json_data['pdf_size']} bytes")

    # 4. CSV to PDF
    print("Testing CSV to PDF conversion route...")
    csv_buf = io.BytesIO(b"Item,Price\nLaptop,1000\nPhone,500\n")
    res = client.post('/convert_to_pdf', data={'file': (csv_buf, 'test_data.csv')}, content_type='multipart/form-data')
    json_data = res.get_json()
    assert res.status_code == 200 and json_data.get('success'), f"CSV to PDF failed: {json_data}"
    print(f"CSV to PDF success! Total pages: {json_data['total_pages']}, PDF size: {json_data['pdf_size']} bytes")

    print("ALL PDF CONVERTER ROUTE TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    test_pdf_converter_routes()
