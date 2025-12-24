"""
Integration tests for deadline calculator with natural language date support.
"""

import unittest
import datetime
from legal_toolkit.deadlines import calculate_cpr_deadline

class TestDeadlineCalculatorWithNaturalLanguage(unittest.TestCase):
    """Test cases for deadline calculator with natural language dates."""
    
    def test_calculate_with_strict_date_format(self):
        """Test deadline calculation with strict YYYY-MM-DD format."""
        result = calculate_cpr_deadline("2024-12-20", "12:00", "england-and-wales")
        
        # Verify structure
        self.assertIsInstance(result, dict)
        self.assertNotIn("error", result)
        
        # Verify data types
        self.assertIsInstance(result['deemed_service'], datetime.date)
        self.assertIsInstance(result['filing_deadline'], datetime.date)

    def test_calculate_with_natural_language_tomorrow(self):
        """Test deadline calculation with 'tomorrow'."""
        result = calculate_cpr_deadline("tomorrow", "14:30", "england-and-wales")
        
        self.assertIsInstance(result, dict)
        self.assertNotIn("error", result)
        
        # Logic Check: Filing deadline must be after deemed service
        self.assertGreater(result['filing_deadline'], result['deemed_service'])
    
    def test_calculate_with_natural_language_alternative_format(self):
        """Test deadline calculation with alternative date format."""
        result = calculate_cpr_deadline("25 Dec 2024", "10:00", "england-and-wales")
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['deemed_service'].year, 2024)
    
    def test_invalid_date_returns_error(self):
        """Test that invalid date input returns an error key."""
        result = calculate_cpr_deadline("not a valid date xyz", "12:00", "england-and-wales")
        
        # Should contain error key
        self.assertIn("error", result)
        # Should NOT contain success data
        self.assertNotIn("deemed_service", result)

if __name__ == '__main__':
    unittest.main()