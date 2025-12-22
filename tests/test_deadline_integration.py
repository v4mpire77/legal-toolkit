"""
Integration tests for deadline calculator with natural language date support.
"""

import unittest
import datetime
from io import StringIO
import sys
from legal_toolkit.deadlines import calculate_cpr_deadline


class TestDeadlineCalculatorWithNaturalLanguage(unittest.TestCase):
    """Test cases for deadline calculator with natural language dates."""
    
    def test_calculate_with_strict_date_format(self):
        """Test deadline calculation with strict YYYY-MM-DD format."""
        # Redirect stdout to capture output
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            calculate_cpr_deadline("2024-12-20", "12:00", "england-and-wales")
            output = captured_output.getvalue()
            
            # Verify that calculation completed without error
            self.assertIn("CPR LEGAL TOOLKIT", output)
            self.assertIn("DEEMED SERVICE DATE", output)
            self.assertIn("FILING DEADLINE", output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_calculate_with_natural_language_tomorrow(self):
        """Test deadline calculation with 'tomorrow'."""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            calculate_cpr_deadline("tomorrow", "14:30", "england-and-wales")
            output = captured_output.getvalue()
            
            # Verify that calculation completed without error
            self.assertIn("CPR LEGAL TOOLKIT", output)
            self.assertIn("DEEMED SERVICE DATE", output)
            self.assertIn("FILING DEADLINE", output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_calculate_with_natural_language_alternative_format(self):
        """Test deadline calculation with alternative date format."""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            calculate_cpr_deadline("25 Dec 2024", "10:00", "england-and-wales")
            output = captured_output.getvalue()
            
            # Verify that calculation completed without error
            self.assertIn("CPR LEGAL TOOLKIT", output)
            self.assertIn("DEEMED SERVICE DATE", output)
            self.assertIn("FILING DEADLINE", output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_invalid_date_shows_error_message(self):
        """Test that invalid date input shows appropriate error message."""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            calculate_cpr_deadline("not a valid date xyz", "12:00", "england-and-wales")
            output = captured_output.getvalue()
            
            # Should show error message
            self.assertIn("Error", output)
            # Should NOT show the deadline calculation output
            self.assertNotIn("DEEMED SERVICE DATE", output)
        finally:
            sys.stdout = sys.__stdout__


if __name__ == '__main__':
    unittest.main()
