# -*- coding: utf-8 -*-
import io
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import base64
from PIL import Image, ImageDraw
from App import app

def make_test_image_b64(color=(200, 160, 140), text="Person"):
    img = Image.new('RGB', (300, 400), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    # Draw head / face
    draw.ellipse([80, 50, 220, 210], fill=color, outline=(50, 50, 50), width=2)
    # Draw eyes
    draw.ellipse([110, 110, 130, 130], fill=(20, 20, 20))
    draw.ellipse([170, 110, 190, 130], fill=(20, 20, 20))
    # Draw smile
    draw.arc([120, 140, 180, 170], start=0, end=180, fill=(150, 30, 30), width=3)
    # Draw body / shoulders
    draw.polygon([(40, 400), (260, 400), (220, 220), (80, 220)], fill=(30, 60, 120))
    
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode('utf-8')

def run_tests():
    print("=== STARTING PHOTO ENGINEERING E2E TESTS ===")
    client = app.test_client()

    # 1. Test GET /
    res = client.get('/')
    assert res.status_code == 200, f"GET / failed: {res.status_code}"
    html = res.data.decode('utf-8')
    assert 'ফটো ইঞ্জিনিয়ারিং' in html, "ফটো ইঞ্জিনিয়ারিং tab missing in index.html"
    assert 'photoEngineeringTab' in html, "photoEngineeringTab missing in index.html"
    print("✔ [1/8] GET / and tab verified successfully")

    # Generate test images
    img1_b64 = make_test_image_b64((210, 170, 150), "Person 1")
    img2_b64 = make_test_image_b64((190, 150, 130), "Person 2")

    # 2. Test Single Passport BD (40x50mm) Portrait
    res = client.post('/photo_engineer/process', json={
        'mode': 'single',
        'size_preset': 'passport_bd',
        'orientation': 'portrait',
        'bg_color': '#1E6091',
        'remove_bg': True,
        'auto_fresh': True,
        'brightness': 10,
        'contrast': 15,
        'smoothness': 25,
        'sharpness': 25,
        'saturation': 10,
        'image1_b64': img1_b64
    })
    assert res.status_code == 200, f"Single Passport BD failed: {res.data}"
    data = res.get_json()
    assert data['success'] is True
    assert data['width_px'] == 472 and data['height_px'] == 591, f"Passport BD dim error: {data['width_px']}x{data['height_px']}"
    assert 'result_b64' in data and data['result_b64'].startswith('data:image/jpeg;base64,')
    passport_b64 = data['result_b64']
    print(f"✔ [2/8] Passport BD (40x50 mm) verified: {data['width_px']}x{data['height_px']} px @ {data['dpi']} DPI")

    # 3. Test Stamp Size (20x25mm)
    res = client.post('/photo_engineer/process', json={
        'mode': 'single',
        'size_preset': 'stamp',
        'orientation': 'portrait',
        'bg_color': '#1E6091',
        'remove_bg': True,
        'auto_fresh': True,
        'image1_b64': img1_b64
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data['width_px'] == 236 and data['height_px'] == 295
    print(f"✔ [3/8] Stamp Size (20x25 mm) verified: {data['width_px']}x{data['height_px']} px")

    # 4. Test 3R, 4R, 10R Sizes
    for preset, expected_w, expected_h in [('3r', 1050, 1500), ('4r', 1200, 1800), ('10r', 3000, 3600)]:
        res = client.post('/photo_engineer/process', json={
            'mode': 'single',
            'size_preset': preset,
            'orientation': 'portrait',
            'bg_color': '#1E6091',
            'remove_bg': False, # fast test
            'auto_fresh': True,
            'image1_b64': img1_b64
        })
        assert res.status_code == 200
        data = res.get_json()
        assert data['width_px'] == expected_w and data['height_px'] == expected_h
        print(f"✔ Size {preset.upper()} verified: {data['width_px']}x{data['height_px']} px")
    print("✔ [4/8] 3R, 4R, 10R Sizes verified successfully")

    # 5. Test Landscape Orientation
    res = client.post('/photo_engineer/process', json={
        'mode': 'single',
        'size_preset': 'passport_bd',
        'orientation': 'landscape',
        'bg_color': '#1E6091',
        'remove_bg': False,
        'auto_fresh': True,
        'image1_b64': img1_b64
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data['width_px'] == 591 and data['height_px'] == 472
    print(f"✔ [5/8] Landscape orientation swap verified: {data['width_px']}x{data['height_px']} px")

    # 6. Test Dual Photo (Joint Photo layout)
    res = client.post('/photo_engineer/process', json={
        'mode': 'dual',
        'dual_layout': 'joint',
        'size_preset': '4r',
        'orientation': 'landscape',
        'bg_color': '#1E6091',
        'remove_bg': True,
        'auto_fresh': True,
        'scale1': 1.0,
        'scale2': 1.0,
        'gap': 0,
        'image1_b64': img1_b64,
        'image2_b64': img2_b64
    })
    assert res.status_code == 200, f"Dual photo joint failed: {res.data}"
    data = res.get_json()
    assert data['width_px'] == 1800 and data['height_px'] == 1200
    print(f"✔ [6/8] Dual Photo Joint Layout verified: {data['width_px']}x{data['height_px']} px")

    # 7. Test Print Sheet Generator (4R and A4)
    res = client.post('/photo_engineer/print_sheet', json={
        'image_b64': passport_b64,
        'sheet_size': '4r',
        'border': True
    })
    assert res.status_code == 200, f"Print sheet 4R failed: {res.data}"
    data = res.get_json()
    assert data['success'] is True
    assert data['sheet_size'] == '4r'
    sheet_b64 = data['sheet_b64']
    print(f"✔ [7/8] 4R Print Sheet verified: {data['width_px']}x{data['height_px']} px")

    # 8. Test Download Endpoint
    res = client.post('/photo_engineer/download', json={
        'image_b64': passport_b64,
        'filename': 'Test_Passport_Photo',
        'format': 'jpg'
    })
    assert res.status_code == 200
    assert res.mimetype == 'image/jpeg'
    assert len(res.data) > 1000
    print(f"✔ [8/8] HD Download endpoint verified: {len(res.data)} bytes")

    print("\n===========================================")
    print("🎉 ALL PHOTO ENGINEERING TESTS PASSED 100%!")
    print("===========================================")

if __name__ == '__main__':
    run_tests()
