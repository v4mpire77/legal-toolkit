"""
Module: Deadline Calculator
Author: Omar
Description: Calculates procedural deadlines based on the Civil Procedure Rules (CPR).

Legal Basis:
    - CPR Part 10.3(1)(b): Acknowledgment of service must be filed 14 days after service of claim form.
    - CPR Part 2.8(5): If a deadline falls on a day the court office is closed (Sat/Sun/Bank Holiday),
      the act is done in time if done on the next day the court office is open.
"""

import datetime
from .holidays import BankHolidayProvider

def calculate_deemed_service(sent_at: datetime.datetime, provider: BankHolidayProvider):
    """
    Calculates Deemed Service based on CPR 6.14 and 6.26.
    
    CPR 6.26: 4:30 PM Cutoff.
    CPR 6.14: Deemed served on the second business day after the effective step.
    """
    # 1. Normalize Sent Date (CPR 6.26)
    cutoff_time = datetime.time(16, 30)
    sent_date = sent_at.date()
    
    is_business = provider.is_business_day(sent_date)
    is_late = sent_at.time() > cutoff_time
    
    print(f"\n[Step 1: CPR 6.26 - Effective Step]")
    print(f"Actual Transmission: {sent_at.strftime('%Y-%m-%d %H:%M')}")
    
    if not is_business or is_late:
        reason = "Non-business day" if not is_business else "After 16:30 cutoff"
        effective_date = provider.next_business_day(sent_date)
        print(f"Adjustment:          Sent {reason}. Effective date moved to next business day.")
    else:
        effective_date = sent_date
        print(f"Adjustment:          None (Sent before 16:30 on a business day).")
    
    print(f"Effective Step Date: {effective_date.strftime('%A, %d %B %Y')}")

    # 2. Calculate Deemed Service (CPR 6.14)
    # Deemed served on the SECOND business day after the effective step
    deemed_date = provider.add_business_days(effective_date, 2)
    
    print(f"\n[Step 2: CPR 6.14 - Deeming Provision]")
    print(f"Rule:                Second business day after effective step.")
    print(f"Legal Authority:     CPR Part 6.14")
    
    # 3. Calculate Filing Deadline (AOS/Defence - 14 Days)
    # CPR 10.3(1)(b)
    base_deadline = deemed_date + datetime.timedelta(days=14)
    final_deadline = base_deadline
    if not provider.is_business_day(base_deadline):
        final_deadline = provider.next_business_day(base_deadline)
        print(f"\n[Step 3: CPR 2.8(5) - Deadline Adjustment]")
        print(f"Condition:           14-day deadline fell on a weekend/holiday.")
        print(f"Filing Deadline:     Moved to {final_deadline.strftime('%A, %d %B %Y')}")
    else:
        print(f"\n[Step 3: CPR 10.3(1)(b) - Standard Deadline]")
        print(f"Filing Deadline:     {final_deadline.strftime('%A, %d %B %Y')}")

    print("-" * 60)
    print(f"DEEMED SERVICE DATE:  {deemed_date.strftime('%A, %d %B %Y')}")
    print(f"FILING DEADLINE:      {final_deadline.strftime('%A, %d %B %Y')}")
    print("-" * 60)
    return deemed_date, final_deadline

def calculate_cpr_deadline(date_str, time_str="12:00", jurisdiction='england-and-wales'):
    """
    Calculates filing deadlines based on CPR.
    """
    provider = BankHolidayProvider(jurisdiction)
    
    try:
        dt_str = f"{date_str} {time_str}"
        sent_at = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Error: Invalid format. Use YYYY-MM-DD and HH:MM")
        return

    print(f"--- CPR LEGAL TOOLKIT: SERVICE & DEADLINES ---")
    print(f"Jurisdiction: {jurisdiction.replace('-', ' ').title()}")
    
    calculate_deemed_service(sent_at, provider)
