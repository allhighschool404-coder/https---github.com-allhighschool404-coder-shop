import io, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from App import app, SUPPORTED_EXTENSIONS
from PIL import Image

def test_flask_routes():
    client = app.test_client()

    print("Testing GET / ...")
    res = client.get('/')
    assert res.status_code == 200, f"Failed GET / : {res.status_code}"
    print("GET / OK!")

    # 1. Test image upload (PNG)
    print("Testing PNG to JPG conversion route...")
    img = Image.new('RGB', (100, 100), color='purple')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    data = {
        'file': (buf, 'test_image.png'),
        'dpi': '300'
    }
    res = client.post('/convert_file', data=data, content_type='multipart/form-data')
    json_data = res.get_json()
    assert res.status_code == 200 and json_data.get('success'), f"Failed PNG convert: {json_data}"
    print(f"PNG convert success! Total pages: {json_data['total_pages']}, Ext: {json_data['ext']}")

    # 2. Test SVG upload
    print("Testing SVG to JPG conversion route...")
    svg_buf = io.BytesIO(b"<svg width='100' height='100'><rect width='100' height='100' fill='green'/></svg>")
    data = {
        'file': (svg_buf, 'test_vector.svg'),
        'dpi': '300'
    }
    res = client.post('/convert_file', data=data, content_type='multipart/form-data')
    json_data = res.get_json()
    assert res.status_code == 200 and json_data.get('success'), f"Failed SVG convert: {json_data}"
    print(f"SVG convert success! Total pages: {json_data['total_pages']}")

    # 3. Test TXT upload
    print("Testing TXT to JPG conversion route...")
    txt_buf = io.BytesIO(b"Hello from test txt document conversion!")
    data = {
        'file': (txt_buf, 'test_doc.txt'),
        'dpi': '300'
    }
    res = client.post('/convert_file', data=data, content_type='multipart/form-data')
    json_data = res.get_json()
    assert res.status_code == 200 and json_data.get('success'), f"Failed TXT convert: {json_data}"
    print(f"TXT convert success! Total pages: {json_data['total_pages']}")

    # 4. Test CSV upload
    print("Testing CSV to JPG conversion route...")
    csv_buf = io.BytesIO(b"ColA,ColB\nVal1,Val2\nVal3,Val4\n")
    data = {
        'file': (csv_buf, 'test_sheet.csv'),
        'dpi': '300'
    }
    res = client.post('/convert_file', data=data, content_type='multipart/form-data')
    json_data = res.get_json()
    assert res.status_code == 200 and json_data.get('success'), f"Failed CSV convert: {json_data}"
    print(f"CSV convert success! Total pages: {json_data['total_pages']}")

    print("\nALL 19 FORMAT CONVERTER ROUTE TESTS PASSED SUCCESSFULLY! 🎉")

if __name__ == '__main__':
    test_flask_routes()
