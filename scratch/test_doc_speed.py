import time
import io
import pandas as pd
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def fast_docx_to_pdf(docx_bytes):
    doc_obj = Document(io.BytesIO(docx_bytes))
    pdf_buf = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buf, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    elements = []
    
    for p in doc_obj.paragraphs:
        if p.text.strip():
            elements.append(Paragraph(p.text.strip(), styles['Normal']))
    for table in doc_obj.tables:
        table_data = []
        for row in table.rows:
            table_data.append([cell.text.strip() for cell in row.cells])
        if table_data:
            t = Table(table_data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4F46E5')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
            ]))
            elements.append(t)
            
    doc.build(elements)
    pdf_buf.seek(0)
    return pdf_buf.getvalue()

def test():
    # Build sample docx
    doc = Document()
    doc.add_heading("Sample Document", level=1)
    for i in range(5):
        doc.add_paragraph(f"Paragraph test {i+1}")
    table = doc.add_table(rows=3, cols=3)
    for r in range(3):
        for c in range(3):
            table.cell(r, c).text = f"Data {r},{c}"
            
    buf = io.BytesIO()
    doc.save(buf)
    docx_bytes = buf.getvalue()

    t0 = time.time()
    pdf_bytes = fast_docx_to_pdf(docx_bytes)
    t1 = time.time()
    print(f"Fast Native DOCX to PDF: {t1 - t0:.4f} seconds (PDF size: {len(pdf_bytes)})")

if __name__ == '__main__':
    test()
