import io
import fitz
from PIL import Image

def test_pdf_conversions():
    # 1. Image to PDF
    img = Image.new('RGB', (600, 800), color='indigo')
    img_buf = io.BytesIO()
    img.save(img_buf, format='JPEG')
    
    pdf_doc = fitz.open()
    page = pdf_doc.new_page(width=600, height=800)
    page.insert_image(fitz.Rect(0, 0, 600, 800), stream=img_buf.getvalue())
    pdf_bytes = pdf_doc.tobytes()
    print("Image to PDF bytes len:", len(pdf_bytes))

    # 2. SVG to PDF
    svg_bytes = b"<svg width='200' height='200'><rect width='200' height='200' fill='red'/></svg>"
    doc = fitz.open(stream=svg_bytes, filetype="svg")
    pdf_bytes_svg = doc.convert_to_pdf()
    print("SVG to PDF bytes len:", len(pdf_bytes_svg))

if __name__ == '__main__':
    test_pdf_conversions()
