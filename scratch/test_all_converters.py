import os
import tempfile
import io
import fitz
import pandas as pd
from PIL import Image

def test_converters():
    # 1. Test image
    img = Image.new('RGB', (200, 200), color='green')
    img_buf = io.BytesIO()
    img.save(img_buf, format='JPEG')
    print("JPEG test ok, size:", len(img_buf.getvalue()))

    # 2. Test SVG
    svg = b"<svg xmlns='http://www.w3.org/2000/svg' width='100' height='100'><rect width='100' height='100' fill='red'/></svg>"
    doc = fitz.open(stream=svg, filetype="svg")
    pix = doc[0].get_pixmap(dpi=300)
    print("SVG test ok, pix width:", pix.width)

    # 3. Test Word COM
    import pythoncom, win32com.client
    pythoncom.CoInitialize()
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        print("Word COM initialized ok")
        word.Quit()
    finally:
        pythoncom.CoUninitialize()

    # 4. Test Excel COM
    pythoncom.CoInitialize()
    try:
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False
        print("Excel COM initialized ok")
        excel.Quit()
    finally:
        pythoncom.CoUninitialize()

if __name__ == '__main__':
    test_converters()
