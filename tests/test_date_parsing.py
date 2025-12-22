"""
Unit tests for natural language date parsing functionality.
"""

import unittest
import datetime
from legal_toolkit.utils import parse_date


class TestDateParsing(unittest.TestCase):
    """Test cases for the parse_date utility function."""
    
    def test_strict_format_yyyy_mm_dd(self):
        """Test parsing strict YYYY-MM-DD format."""
        result = parse_date("2024-12-25")
        expected = datetime.date(2024, 12, 25)
        self.assertEqual(result, expected)
    
    def test_alternative_date_format(self):
        """Test parsing alternative date formats."""
        result = parse_date("25 Dec 2024")
        expected = datetime.date(2024, 12, 25)
        self.assertEqual(result, expected)
    
    def test_natural_language_tomorrow(self):
        """Test parsing 'tomorrow'."""
        result = parse_date("tomorrow")
        expected = datetime.date.today() + datetime.timedelta(days=1)
        self.assertEqual(result, expected)
    
    def test_natural_language_today(self):
        """Test parsing 'today'."""
        result = parse_date("today")
        expected = datetime.date.today()
        self.assertEqual(result, expected)
    
    def test_natural_language_next_friday(self):
        """Test parsing 'Friday' (interpreted as next Friday with future preference)."""
        result = parse_date("Friday")
        # Result should be a date object and should be a Friday
        self.assertIsInstance(result, datetime.date)
        self.assertEqual(result.weekday(), 4)  # Friday is weekday 4
        # Should be in the future or today (if today is Friday)
        self.assertGreaterEqual(result, datetime.date.today())
    
    def test_natural_language_in_3_days(self):
        """Test parsing 'in 3 days'."""
        result = parse_date("in 3 days")
        expected = datetime.date.today() + datetime.timedelta(days=3)
        self.assertEqual(result, expected)
    
    def test_empty_string_raises_error(self):
        """Test that empty string raises ValueError."""
        with self.assertRaises(ValueError):
            parse_date("")
    
    def test_none_raises_error(self):
        """Test that None raises ValueError."""
        with self.assertRaises(ValueError):
            parse_date(None)
    
    def test_invalid_input_raises_error(self):
        """Test that completely invalid input raises ValueError."""
        with self.assertRaises(ValueError):
            parse_date("not a date at all xyz123")
    
    def test_numeric_input(self):
        """Test that numeric input raises ValueError."""
        with self.assertRaises(ValueError):
            parse_date(12345)


if __name__ == '__main__':
    unittest.main()
