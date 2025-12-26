import datetime
from legal_toolkit.deadlines import calculate_deemed_service
from legal_toolkit.holidays import BankHolidayProvider

def test_agreed_extension_logic():
    provider = BankHolidayProvider('england-and-wales')
    # Wed, Dec 24, 2025 at 10:00 AM
    sent_at = datetime.datetime(2025, 12, 24, 10, 0)
    
    # Standard: Deemed service = Friday Dec 26 (Holiday) -> Monday Dec 29
    # Deadline = Monday Dec 29 + 14 days = Monday Jan 12
    # With 28 day extension = Monday Jan 12 + 28 days = Monday Feb 9
    
    deemed, deadline = calculate_deemed_service(sent_at, provider, extension_days=28)
    
    # 14 + 28 = 42 days from deemed service
    expected_deadline = deemed + datetime.timedelta(days=42)
    
    assert deadline == expected_deadline
    assert (deadline - deemed).days == 42
