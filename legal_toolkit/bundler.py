"""
Module: Bundle Indexer
Author: Omar
Description: Generates an index for court bundles and checks compliance with
             CPR Practice Direction 5B regarding email size limits.
             
Legal Basis:
    - CPR PD 5B para 2.1(1): Total email size limit 25MB for general filing.
    - CPR PD 5B para 2.1(2): Total email size limit 10MB for County Court filing.
"""

import os
import datetime
from .utils import format_bytes

def generate_bundle_index(directory, court_type='general'):
    """
    Generates an index of files in the specified directory and checks for size compliance.
    
    Args:
        directory (str): Path to the directory to index.
        court_type (str): 'general' (25MB limit) or 'county' (10MB limit).
    """
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return

    # Define limits based on PD 5B
    # 25MB in bytes = 25 * 1024 * 1024
    # 10MB in bytes = 10 * 1024 * 1024
    LIMITS = {
        'general': 25 * 1024 * 1024,
        'county': 10 * 1024 * 1024
    }
    
    limit = LIMITS.get(court_type, LIMITS['general'])
    limit_name = "25MB (General/High Court)" if court_type == 'general' else "10MB (County Court)"

    files = os.listdir(directory)
    ignored_files = ['indexer.py', 'INDEX.txt', '__pycache__']
    
    # Filter and sort files (excluding hidden files)
    files = [f for f in files if f not in ignored_files and not f.startswith('.')]
    files.sort()
    
    output_lines = []
    output_lines.append(f"COURT BUNDLE INDEX (v2.0)")
    output_lines.append(f"Target Court: {limit_name}")
    output_lines.append(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output_lines.append("-" * 70)
    output_lines.append(f"{'#':<3} | {'File Name':<45} | {'Size':<10}")
    output_lines.append("-" * 70)
    
    total_size = 0
    
    for idx, filename in enumerate(files, start=1):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            total_size += file_size
            
            readable_size = format_bytes(file_size)
            output_lines.append(f"{idx:<3} | {filename:<45} | {readable_size:<10}")
    
    output_lines.append("-" * 70)
    output_lines.append(f"TOTAL FILES: {len(files)}")
    output_lines.append(f"TOTAL BUNDLE SIZE: {format_bytes(total_size)}")
    
    # Compliance Check (CPR PD 5B)
    output_lines.append("-" * 70)
    if total_size > limit:
        output_lines.append(f"!!! WARNING: Bundle exceeds {limit_name} email limit !!!")
        output_lines.append(f"    Legal Basis: CPR Practice Direction 5B para 2.1")
        output_lines.append(f"    Action Required: Split bundle or use alternative transfer method.")
    else:
        output_lines.append(f"✓ Bundle is within {limit_name} email limit.")
    
    # Output to file
    output_path = os.path.join(directory, 'INDEX.txt')
    with open(output_path, 'w') as f:
        f.write('\n'.join(output_lines))
    
    print('\n'.join(output_lines))
    print(f"\nIndex saved to: {output_path}")
