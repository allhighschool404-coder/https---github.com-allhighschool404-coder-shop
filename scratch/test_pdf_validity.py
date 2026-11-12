import io, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import fitz
import docx
from App import convert_any_file_to_pdf, convert_doc_via_word

def test_pdf_header():
    # 1. Create a Word document
    doc = docx.Document()
    doc.add_heading('Test Science Document', 0)
    doc.add_paragraph('Science chapter lesson plan content.')
    
    docx_buf = io.BytesIO()
    doc.save(docx_buf)
    docx_bytes = docx_buf.getvalue()

    # Convert to PDF
    pdf_bytes = convert_any_file_to_pdf(docx_bytes, '8-hy-sci-abcd-0712 Ok.docx')
    
    print("PDF bytes length:", len(pdf_bytes))
    print("PDF Header:", pdf_bytes[:10])
    
    # Check if starts with %PDF-
    assert pdf_bytes.startswith(b'%PDF-'), "PDF does not start with %PDF- header!"
    
    # Verify opening with PyMuPDF
    fitz_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    print("PyMuPDF opened PDF successfully! Total pages:", len(fitz_doc))
    fitz_doc.close()
    
    print("PDF VALIDITY TEST PASSED!")

if __name__ == '__main__':
    test_pdf_header()
