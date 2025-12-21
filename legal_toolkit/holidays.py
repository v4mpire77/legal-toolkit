"""
Module: Bank Holiday Provider
Description: Fetches and caches UK Bank Holidays from GOV.UK for CPR compliance.
             Implements the "Resilient Provider" pattern (Cache-first with local fallback).
"""

import os
import json
import requests
import datetime
from typing import Set

class BankHolidayProvider:
    API_URL = "https://www.gov.uk/bank-holidays.json"
    
    def __init__(self, jurisdiction: str = 'england-and-wales'):
        """
        Initialize the provider for a specific jurisdiction.
        Options: 'england-and-wales', 'scotland', 'northern-ireland'
        """
        self.jurisdiction = jurisdiction
        self.cache_dir = os.path.join(os.path.expanduser("~"), ".legal_toolkit")
        self.cache_file = os.path.join(self.cache_dir, "bank_holidays_cache.json")
        self.seed_file = os.path.join(os.path.dirname(__file__), "bank_holidays.json")
        
        # Ensure cache directory exists
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
            
        self.holidays = self._load_data()

    def _load_data(self) -> Set[datetime.date]:
        """
        Loads holiday data. Prioritizes fresh API data; falls back to cache then seed.
        """
        data = None
        
        # 1. Try Network Refresh
        try:
            # 3 second timeout to prevent hanging in courtrooms/trains
            response = requests.get(self.API_URL, timeout=3.0)
            response.raise_for_status()
            data = response.json()
            # Update cache
            with open(self.cache_file, 'w') as f:
                json.dump(data, f)
        except (requests.RequestException, json.JSONDecodeError):
            # 2. Fallback to Local Cache
            if os.path.exists(self.cache_file):
                try:
                    with open(self.cache_file, 'r') as f:
                        data = json.load(f)
                except json.JSONDecodeError:
                    pass
            
            # 3. Fallback to Shipped Seed File
            if not data and os.path.exists(self.seed_file):
                with open(self.seed_file, 'r') as f:
                    data = json.load(f)

        if not data or self.jurisdiction not in data:
            return set()

        # Parse dates into datetime.date objects for O(1) lookup
        events = data[self.jurisdiction].get('events', [])
        return {datetime.datetime.strptime(e['date'], '%Y-%m-%d').date() for e in events}

    def is_holiday(self, date_obj: datetime.date) -> bool:
        """Checks if a date is a bank holiday in the selected jurisdiction."""
        return date_obj in self.holidays

    def is_business_day(self, date_obj: datetime.date) -> bool:
        """Checks if a date is a business day (not Sat, Sun, or Bank Holiday)."""
        # weekday(): 0=Mon, 5=Sat, 6=Sun
        if date_obj.weekday() >= 5:
            return False
        return not self.is_holiday(date_obj)

    def next_business_day(self, date_obj: datetime.date) -> datetime.date:
        """Calculates the next available business day."""
        current = date_obj + datetime.timedelta(days=1)
        while not self.is_business_day(current):
            current += datetime.timedelta(days=1)
        return current

    def add_business_days(self, start_date: datetime.date, days_to_add: int) -> datetime.date:
        """Adds a specific number of business days to a date."""
        current = start_date
        for _ in range(days_to_add):
            current = self.next_business_day(current)
        return current
