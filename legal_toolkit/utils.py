"""
Shared utility functions for the Legal Toolkit.
"""

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
