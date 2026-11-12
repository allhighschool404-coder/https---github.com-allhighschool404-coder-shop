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

def process_pillow_to_pdf(file_bytes):
    img = Image.open(io.BytesIO(file_bytes))
    try:
        n_frames = getattr(img, 'n_frames', 1)
    except Exception:
        n_frames = 1

    pdf_doc = fitz.open()
    for i in range(n_frames):
        try:
            img.seek(i)
        except EOFError:
            break
            
        frame = img.copy()
        if frame.mode in ('RGBA', 'LA', 'P'):
            frame = frame.convert('RGBA')
            background = Image.new('RGB', frame.size, (255, 255, 255))
            background.paste(frame, mask=frame.split()[3])
            rgb_img = background
        else:
            rgb_img = frame.convert('RGB')

        out_buf = io.BytesIO()
        rgb_img.save(out_buf, format='JPEG', quality=95)
        img_data = out_buf.getvalue()
        
        page = pdf_doc.new_page(width=rgb_img.width, height=rgb_img.height)
        page.insert_image(fitz.Rect(0, 0, rgb_img.width, rgb_img.height), stream=img_data)

    img.close()
    pdf_bytes = pdf_doc.tobytes()
    pdf_doc.close()
    return pdf_bytes

def convert_any_file_to_pdf(file_bytes, filename):
    ext = os.path.splitext(filename)[1].lower()
    if not ext:
        ext = '.pdf'

    # 1. PDF
    if ext == '.pdf':
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        pdf_bytes = doc.tobytes()
        doc.close()
        return pdf_bytes

    # 2. SVG
    if ext == '.svg':
        doc = fitz.open(stream=file_bytes, filetype="svg")
        pdf_bytes = doc.convert_to_pdf()
        doc.close()
        return pdf_bytes

    # 3. Image formats (.jpeg, .jpg, .png, .webp, .gif, .psd)
    if ext in ['.jpeg', '.jpg', '.png', '.webp', '.gif', '.psd']:
        try:
            return process_pillow_to_pdf(file_bytes)
        except Exception:
            doc = fitz.open(stream=file_bytes)
            pdf_bytes = doc.convert_to_pdf()
            doc.close()
            return pdf_bytes

    # 4. Vector Graphics (.ai, .eps)
    if ext in ['.ai', '.eps']:
        try:
            doc = fitz.open(stream=file_bytes)
            pdf_bytes = doc.convert_to_pdf()
            doc.close()
            return pdf_bytes
        except Exception:
            pass
        try:
            return process_pillow_to_pdf(file_bytes)
        except Exception as e:
            raise RuntimeError(f"Could not convert {ext} to PDF: {e}")

    # 5. Documents (.doc, .docx, .rtf, .odt, .txt)
    if ext in ['.doc', '.docx', '.rtf', '.odt', '.txt']:
        # Import COM function from App if needed
        if ext == '.txt':
            try:
                doc = fitz.open(stream=file_bytes, filetype="txt")
                pdf_bytes = doc.convert_to_pdf()
                doc.close()
                return pdf_bytes
            except Exception:
                pass
        raise NotImplementedError("Office docs test")

    # 6. Spreadsheets (.xls, .xlsx, .csv, .xlsm, .ods)
    if ext in ['.xls', '.xlsx', '.csv', '.xlsm', '.ods']:
        raise NotImplementedError("Spreadsheets test")

def test():
    img = Image.new('RGB', (300, 300), color='teal')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    pdf = convert_any_file_to_pdf(buf.getvalue(), 'sample.png')
    print("PNG to PDF test passed, output PDF size:", len(pdf))

test()
