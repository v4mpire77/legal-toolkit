import pytest
import datetime
from legal_toolkit.deadlines import calculate_deemed_service
from legal_toolkit.holidays import BankHolidayProvider

# Mock Provider for consistent testing (ignoring actual bank holiday API calls)
class MockBankHolidayProvider(BankHolidayProvider):
    def __init__(self):
        # Initialize with a fixed jurisdiction, but we'll override methods
        super().__init__('england-and-wales')
        # Hardcode some known bank holidays for testing
        # 2023-12-25 (Xmas), 2023-12-26 (Boxing Day), 2024-01-01 (New Year)
        self.holidays = {
            datetime.date(2023, 12, 25),
            datetime.date(2023, 12, 26),
            datetime.date(2024, 1, 1)
        }

    def is_business_day(self, date_obj):
        if date_obj.weekday() >= 5: # Sat=5, Sun=6
            return False
        if date_obj in self.holidays:
            return False
        return True

@pytest.fixture
def provider():
    return MockBankHolidayProvider()

def test_standard_service(provider):
    """
    Standard Case: Sent Tuesday 1pm -> Deemed Thursday.
    """
    sent_at = datetime.datetime(2023, 10, 3, 13, 0) # Tuesday
    deemed, deadline = calculate_deemed_service(sent_at, provider)
    
    assert deemed == datetime.date(2023, 10, 5) # Thursday (Day 2)

def test_cutoff_time(provider):
    """
    CPR 6.26: Sent after 4:30pm (16:30) is treated as sent next business day.
    Sent Tuesday 17:00 -> Effective Wednesday -> Deemed Friday.
    """
    sent_at = datetime.datetime(2023, 10, 3, 17, 0) # Tuesday 5pm
    deemed, deadline = calculate_deemed_service(sent_at, provider)
    
    # Effective Step: Wed 4th
    # Day 1: Thu 5th
    # Day 2: Fri 6th
    assert deemed == datetime.date(2023, 10, 6)

def test_weekend_service(provider):
    """
    Sent Saturday -> Effective Monday -> Deemed Wednesday.
    """
    sent_at = datetime.datetime(2023, 10, 7, 10, 0) # Saturday
    deemed, deadline = calculate_deemed_service(sent_at, provider)
    
    # Effective Step: Mon 9th
    # Day 1: Tue 10th
    # Day 2: Wed 11th
    assert deemed == datetime.date(2023, 10, 11)

def test_filing_deadline_standard(provider):
    """
    CPR 10.3(1)(b): 14 days after deemed service.
    Deemed Thu 5th Oct -> Deadline Thu 19th Oct.
    """
    sent_at = datetime.datetime(2023, 10, 3, 13, 0) # Tue -> Deemed Thu 5th
    deemed, deadline = calculate_deemed_service(sent_at, provider)
    
    assert deadline == datetime.date(2023, 10, 19)

def test_filing_deadline_weekend_adjustment(provider):
    """
    CPR 2.8(5): If deadline ends on Sat/Sun, move to next business day.
    Deemed Service: Sat 23rd Sept (Hypothetical) -> Deadline Sat 7th Oct -> Mon 9th Oct.
    """
    # We need to reverse engineer a sent date to land deemed service on a specific date 
    # OR we can just test the logic if we could isolate it, but here we integration test it.
    
    # Let's try: Sent Wed 20th Sept 1pm -> Deemed Fri 22nd Sept.
    # Deadline = Fri 22nd + 14 days = Fri 6th Oct. (Standard)
    
    # Sent Thu 21st Sept 1pm -> Deemed Mon 25th Sept (Fri=1, Mon=2).
    # Deadline = Mon 25th + 14 = Mon 9th Oct.
    
    # Let's try a case where 14 days lands on Saturday.
    # We need Deemed Date to be Saturday? No, deemed date is always a business day per CPR 6.14?
    # Actually CPR 6.14 says "second business day". So Deemed Date is ALWAYS a business day.
    
    # However, 14 days from a business day CAN be a weekend.
    # Example: Deemed Friday 1st. + 14 days = Friday 15th.
    # Example: Deemed Monday 4th. + 14 days = Monday 18th.
    # It seems 14 days usually preserves the day of week?
    # Fri + 14 = Fri. Mon + 14 = Mon.
    
    # So when does the weekend adjustment happen for 14 day deadlines?
    # Only if the deemed date was somehow calculated incorrectly or if a Bank Holiday interferes.
    
    # Example: Deemed Monday 25th Dec (Xmas - but deemed must be business day).
    # Let's say Deemed is Tue 12th Dec. + 14 = Tue 26th Dec (Boxing Day - Holiday).
    # Deadline should move to Wed 27th.
    
    sent_at = datetime.datetime(2023, 12, 8, 13, 0) # Fri 8th Dec
    # Effective: Fri 8th.
    # Deemed: Tue 12th Dec (Mon 11th is day 1).
    
    deemed, deadline = calculate_deemed_service(sent_at, provider)
    
    assert deemed == datetime.date(2023, 12, 12)
    # 12th + 14 = 26th (Boxing Day).
    # Should move to next business day (27th).
    assert deadline == datetime.date(2023, 12, 27)

