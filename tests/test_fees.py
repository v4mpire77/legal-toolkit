import unittest
from legal_toolkit.fees import calculate_issue_fee

class TestFeeCalculator(unittest.TestCase):

    def test_lower_brackets(self):
        """Test fixed fee brackets (Up to 10k)"""
        self.assertEqual(calculate_issue_fee(300), "£35")
        self.assertEqual(calculate_issue_fee(500), "£50")
        self.assertEqual(calculate_issue_fee(1000), "£70")
        self.assertEqual(calculate_issue_fee(5000), "£205")
        self.assertEqual(calculate_issue_fee(10000), "£455")

    def test_percentage_rule(self):
        """Test the 5% rule for claims between 10k and 200k"""
        # 15,000 * 0.05 = 750
        self.assertEqual(calculate_issue_fee(15000), "£750.00")
        # 100,000 * 0.05 = 5,000
        self.assertEqual(calculate_issue_fee(100000), "£5,000.00")

    def test_max_cap(self):
        """Test the £10,000 cap for claims over 200k"""
        # Note: The original logic in fees.py returns "£10,000.00" for 200k because it falls into the 5% bucket logic
        # but 200,000 * 0.05 is exactly 10,000. So we expect the formatted string.
        self.assertEqual(calculate_issue_fee(200000), "£10,000.00") 
        self.assertEqual(calculate_issue_fee(250000), "£10,000")    # Over boundary

    def test_invalid_input(self):
        """Test negative or zero values"""
        self.assertEqual(calculate_issue_fee(0), "Invalid claim value")
        self.assertEqual(calculate_issue_fee(-100), "Invalid claim value")

if __name__ == '__main__':
    unittest.main()