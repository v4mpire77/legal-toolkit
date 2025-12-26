import fitz
from legal_toolkit.audit import AuditGenerator

def test_audit_report_generation():
    gen = AuditGenerator()
    case_data = {
        "title": "Smith v Jones",
        "case_type": "deadline",
        "created_at": "2025-12-25T10:00:00",
        "data": {
            "sent_at": "2025-12-20T14:00:00",
            "deemed_service": "2025-12-23T14:00:00",
            "deadline": "2026-01-06T14:00:00",
            "extension_days": 14
        }
    }
    
    pdf_bytes = gen.generate_report(case_data, "test@example.com")
    
    assert pdf_bytes is not None
    assert len(pdf_bytes) > 0
    assert b"%PDF" in pdf_bytes
    
    # Analyze content
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = doc[0].get_text()
    
    assert "LEGAL TOOLKIT: COMPLIANCE AUDIT" in text
    assert "Smith v Jones" in text
    assert "test@example.com" in text
    assert "Agreed Extension" in text
    assert "14 Days" in text
