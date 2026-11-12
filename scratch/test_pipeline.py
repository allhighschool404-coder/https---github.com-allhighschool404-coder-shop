import os
import tempfile
import io
import fitz
import pandas as pd
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def process_fitz_doc(doc, dpi=300, quality=95):
    pages_data = []
    for i in range(len(doc)):
        page = doc.load_page(i)
        pix = page.get_pixmap(dpi=dpi, alpha=False)
        pages_data.append((pix.width, pix.height))
    doc.close()
    return pages_data

def process_pillow_image(file_bytes, dpi=300, quality=95):
    img = Image.open(io.BytesIO(file_bytes))
    return [(img.width, img.height)]

def test():
    # Test image
    img = Image.new('RGB', (150, 150), color='blue')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    pages = process_pillow_image(buf.getvalue())
    print("Pillow test result:", pages)

    # Test fitz SVG
    svg = b"<svg width='100' height='100'><rect width='100' height='100' fill='black'/></svg>"
    doc = fitz.open(stream=svg, filetype="svg")
    pages_svg = process_fitz_doc(doc)
    print("SVG test result:", pages_svg)

test()
