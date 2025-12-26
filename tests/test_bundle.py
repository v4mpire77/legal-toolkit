import os
import fitz
from legal_toolkit.pdf_engine import PDFEngine

def test_bundle_with_hyperlinked_index():
    engine = PDFEngine()
    input_files = ["tests/sample_pdfs/doc1.pdf", "tests/sample_pdfs/doc2.pdf"]
    output_path = "tests/sample_pdfs/test_bundle.pdf"
    
    if os.path.exists(output_path):
        os.remove(output_path)
        
    engine.merge_pdfs(input_files, output_path, bates_prefix="TEST")
    
    assert os.path.exists(output_path)
    
    doc = fitz.open(output_path)
    # Page 1 should be the index
    # Page 2 should be doc1
    # Page 3 should be doc2
    assert len(doc) == 3
    
    # Check for text on index page
    index_page = doc[0]
    text = index_page.get_text()
    assert "INDEX OF DOCUMENTS" in text
    assert "doc1.pdf" in text
    assert "doc2.pdf" in text
    
    # Check for links on index page
    links = list(index_page.links())
    assert len(links) >= 2
    
    # First link should point to page 1 (which is doc1, the second page in doc)
    assert links[0]["page"] == 1
    assert links[1]["page"] == 2
    
    # Check Bates stamping on last page
    last_page = doc[2]
    assert "TEST-000003" in last_page.get_text()
    
    doc.close()
