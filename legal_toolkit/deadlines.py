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
import logging
from .holidays import BankHolidayProvider
from .utils import parse_date

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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
    
    logger.info(f"[Step 1: CPR 6.26 - Effective Step]")
    logger.info(f"Actual Transmission: {sent_at.strftime('%Y-%m-%d %H:%M')}")
    
    if not is_business or is_late:
        reason = "Non-business day" if not is_business else "After 16:30 cutoff"
        effective_date = provider.next_business_day(sent_date)
        logger.info(f"Adjustment:          Sent {reason}. Effective date moved to next business day.")
    else:
        effective_date = sent_date
        logger.info(f"Adjustment:          None (Sent before 16:30 on a business day).")
    
    logger.info(f"Effective Step Date: {effective_date.strftime('%A, %d %B %Y')}")

    # 2. Calculate Deemed Service (CPR 6.14)
    # Deemed served on the SECOND business day after the effective step
    deemed_date = provider.add_business_days(effective_date, 2)
    
    logger.info(f"[Step 2: CPR 6.14 - Deeming Provision]")
    logger.info(f"Rule:                Second business day after effective step.")
    logger.info(f"Legal Authority:     CPR Part 6.14")
    
    # 3. Calculate Filing Deadline (AOS/Defence - 14 Days)
    # CPR 10.3(1)(b)
    base_deadline = deemed_date + datetime.timedelta(days=14)
    final_deadline = base_deadline
    if not provider.is_business_day(base_deadline):
        final_deadline = provider.next_business_day(base_deadline)
        logger.info(f"[Step 3: CPR 2.8(5) - Deadline Adjustment]")
        logger.info(f"Condition:           14-day deadline fell on a weekend/holiday.")
        logger.info(f"Filing Deadline:     Moved to {final_deadline.strftime('%A, %d %B %Y')}")
    else:
        logger.info(f"[Step 3: CPR 10.3(1)(b) - Standard Deadline]")
        logger.info(f"Filing Deadline:     {final_deadline.strftime('%A, %d %B %Y')}")

    logger.info("-" * 60)
    logger.info(f"DEEMED SERVICE DATE:  {deemed_date.strftime('%A, %d %B %Y')}")
    logger.info(f"FILING DEADLINE:      {final_deadline.strftime('%A, %d %B %Y')}")
    logger.info("-" * 60)
    return deemed_date, final_deadline

def calculate_cpr_deadline(date_str, time_str="12:00", jurisdiction='england-and-wales'):
    """
    Calculates filing deadlines based on CPR.
    
    Args:
        date_str (str): Date of transmission. Can be in strict format (YYYY-MM-DD) 
                       or natural language (e.g., "next Friday", "tomorrow", "25 Dec 2024").
        time_str (str): Time of transmission in HH:MM format (default: "12:00").
        jurisdiction (str): Jurisdiction for bank holidays.
    """
    provider = BankHolidayProvider(jurisdiction)
    
    try:
        # Use the new parse_date helper for flexible date parsing
        date_obj = parse_date(date_str)
        
        # Parse time separately
        time_obj = datetime.datetime.strptime(time_str, "%H:%M").time()
        
        # Combine date and time
        sent_at = datetime.datetime.combine(date_obj, time_obj)
    except ValueError as e:
        logger.error(f"Error: {str(e)}")
        logger.info("Please use a valid date format (e.g., 'YYYY-MM-DD', 'tomorrow', 'Friday')")
        return

    logger.info(f"--- CPR LEGAL TOOLKIT: SERVICE & DEADLINES ---")
    logger.info(f"Jurisdiction: {jurisdiction.replace('-', ' ').title()}")
    
    calculate_deemed_service(sent_at, provider)