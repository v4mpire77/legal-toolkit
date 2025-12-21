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

def next_working_day(date_obj):
    """
    Adjusts a date to the next working day if it falls on a weekend.
    
    Args:
        date_obj (datetime.date): The date to check. 
    
    Returns:
        datetime.date: The adjusted date (Monday) or the original date.
        bool: True if adjusted, False otherwise.
    """
    # weekday(): 0=Mon, 5=Sat, 6=Sun
    original = date_obj
    if date_obj.weekday() == 5:  # Saturday
        date_obj += datetime.timedelta(days=2)
    elif date_obj.weekday() == 6:  # Sunday
        date_obj += datetime.timedelta(days=1)
    
    return date_obj, (date_obj != original)

def calculate_cpr_deadline(service_date_str):
    """
    Calculates the 14-day deadline for Acknowledgment of Service / Defence. 
    
    Args:
        service_date_str (str): Date of service in YYYY-MM-DD format.
    """
    print(f"--- CPR DEADLINE CALCULATOR (Civil Procedure Rules) ---")
    
    try:
        service_date = datetime.datetime.strptime(service_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD (e.g., 2025-12-20)")
        return

    # CPR 10.3(1)(b) - 14 days
    base_deadline = service_date + datetime.timedelta(days=14)
    
    print(f"\n[Calculations]")
    print(f"Service Date:       {service_date.strftime('%A, %d %B %Y')}")
    print(f"Standard +14 Days:  {base_deadline.strftime('%A, %d %B %Y')}")
    print(f"Legal Authority:    CPR Part 10.3(1)(b)")

    # CPR 2.8(5) - Weekend/Closed Office check
    final_deadline, adjusted = next_working_day(base_deadline)

    if adjusted:
        print(f"\n[Adjustment Applied]")
        print(f"Condition:          Deadline fell on a weekend.")
        print(f"Legal Authority:    CPR Part 2.8(5) 'Time expires on a day court office is closed'")
        print(f"Adjustment:         Moved to next working day.")
    
    print("-" * 60)
    print(f"OFFICIAL FILING DEADLINE: {final_deadline.strftime('%A, %d %B %Y')}")
    print("-" * 60)
    print("NOTE: This tool automatically adjusts for Weekends.")
    print("      Please manually verify if the deadline falls on a UK Bank Holiday,")
    print("      as CPR 2.8(5) also applies to those days.")
