import io, sys, os, base64
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from App import app, convert_any_file_to_pdf
import fitz
import docx

def test_full_pdf_flow():
    client = app.test_client()

    # Create a docx document named '8-hy-sci-abcd-0712 Ok.docx'
    doc = docx.Document()
    doc.add_heading('Science Subject Exam Question', 0)
    doc.add_paragraph('This is a test science question paper.')
    
    docx_buf = io.BytesIO()
    doc.save(docx_buf)
    docx_bytes = docx_buf.getvalue()

    # Test POST /convert_to_pdf
    res = client.post('/convert_to_pdf', data={'file': (io.BytesIO(docx_bytes), '8-hy-sci-abcd-0712    Ok.docx')}, content_type='multipart/form-data')
    json_data = res.get_json()
    assert res.status_code == 200 and json_data.get('success'), f"Conversion failed: {json_data}"
    
    pdf_b64 = json_data['pdf_b64']
    pdf_bytes = base64.b64decode(pdf_b64)
    
    print("Cleaned filename:", json_data['file_name'])
    print("Decoded PDF bytes len:", len(pdf_bytes))
    assert pdf_bytes.startswith(b'%PDF-'), "Downloaded PDF bytes corrupt!"

    # Verify PyMuPDF opens decoded bytes
    fitz_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    print("PyMuPDF verified pages:", len(fitz_doc))
    fitz_doc.close()

    print("FULL PDF FLOW TEST PASSED PERFECTLY!")

if __name__ == '__main__':
    test_full_pdf_flow()
