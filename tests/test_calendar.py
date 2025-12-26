import datetime
from legal_toolkit.calendar import generate_cpr_ics

def test_generate_cpr_ics():
    sent_at = datetime.datetime(2025, 12, 25, 12, 0)
    deemed = datetime.datetime(2025, 12, 27, 12, 0)
    deadline = datetime.datetime(2026, 1, 10, 12, 0)
    
    ics_content = generate_cpr_ics(sent_at, deemed, deadline)
    
    assert "BEGIN:VCALENDAR" in ics_content
    assert "📄 CPR: Document Transmission" in ics_content
    assert "✅ CPR: Deemed Service" in ics_content
    assert "🚨 CPR FILING DEADLINE" in ics_content
    assert "END:VCALENDAR" in ics_content
    
    # Check if dates are present (ics format usually YYYYMMDD)
    assert "20251225" in ics_content
    assert "20251227" in ics_content
    assert "20260110" in ics_content
