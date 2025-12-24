"""
Module: Court Fees
Description: Calculates Civil Court Issue Fees based on claim value (Form EX50).
"""

def calculate_issue_fee(claim_value: float) -> str:
    """
    Calculates the court issue fee for a money claim.
    Source: HMCTS Form EX50 (Civil Court Fees).
    """
    if claim_value <= 0:
        return "Invalid claim value"
    elif claim_value <= 300:
        return "£35"
    elif claim_value <= 500:
        return "£50"
    elif claim_value <= 1000:
        return "£70"
    elif claim_value <= 1500:
        return "£80"
    elif claim_value <= 3000:
        return "£115"
    elif claim_value <= 5000:
        return "£205"
    elif claim_value <= 10000:
        return "£455"
    elif claim_value <= 200000:
        # For claims between 10k and 200k, fee is 5%
        fee = claim_value * 0.05
        return f"£{fee:,.2f}"
    else:
        # Cap for claims over 200k
        return "£10,000"
