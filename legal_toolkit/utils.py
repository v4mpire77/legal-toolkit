"""
Shared utility functions for the Legal Toolkit.
"""

import datetime
import dateparser

def parse_date(input_str):
    """
    Parse a date string using natural language processing.
    
    Supports both strict formats (YYYY-MM-DD) and natural language inputs 
    like "next Friday", "25 Dec 2024", or "tomorrow".
    
    Args:
        input_str (str): The date string to parse.
    
    Returns:
        datetime.date: Parsed date object.
    
    Raises:
        ValueError: If the date string cannot be parsed.
    
    Examples:
        >>> parse_date("2024-12-25")
        datetime.date(2024, 12, 25)
        >>> parse_date("next Friday")
        # Returns the date of the next Friday
        >>> parse_date("tomorrow")
        # Returns tomorrow's date
    """
    if not input_str or not isinstance(input_str, str):
        raise ValueError("Input must be a non-empty string")
    
    # Try parsing with dateparser
    parsed_datetime = dateparser.parse(
        input_str,
        settings={
            'PREFER_DATES_FROM': 'future',
            'STRICT_PARSING': False,
            'RETURN_AS_TIMEZONE_AWARE': False
        }
    )
    
    if parsed_datetime is None:
        raise ValueError(f"Unable to parse date from: '{input_str}'")
    
    return parsed_datetime.date()

def format_bytes(size, factor=1024, suffix="B"):
    """
    Scale bytes to its proper format (e.g., 1253656 => '1.20MB').
    
    Args:
        size (int): Size in bytes.
        factor (int): Scaling factor (default 1024).
        suffix (str): Suffix for the unit (default "B").
    
    Returns:
        str: Formatted string representing the size.
    """
    for unit in ["", "K", "M", "G", "T", "P"]:
        if size < factor:
            return f"{size:.2f}{unit}{suffix}"
        size /= factor
    return f"{size:.2f}P{suffix}"
