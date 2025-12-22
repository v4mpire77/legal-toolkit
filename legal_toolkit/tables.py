"""
Module: Table Extraction
Description: Extract structured tables from PDFs using pdfplumber.
             Returns tables as Pandas DataFrames for easy analysis.
"""

import pdfplumber
import pandas as pd
from typing import List


def extract_tables(pdf_path: str) -> List[pd.DataFrame]:
    """
    Extracts all tables from a PDF file and returns them as a list of DataFrames.
    
    Args:
        pdf_path: Path to the PDF file to extract tables from.
        
    Returns:
        A list of pandas DataFrames, one for each table found in the PDF.
        Empty list if no tables are found.
        
    Example:
        >>> tables = extract_tables("schedule_of_loss.pdf")
        >>> for i, df in enumerate(tables):
        >>>     print(f"Table {i+1}:")
        >>>     print(df.to_string())
    """
    tables = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract tables from the page
            page_tables = page.extract_tables()
            
            if page_tables:
                for table in page_tables:
                    # Convert to DataFrame
                    # First row is typically the header
                    if len(table) > 1:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        tables.append(df)
                    elif len(table) == 1:
                        # Single row table, no header
                        df = pd.DataFrame(table)
                        tables.append(df)
    
    return tables
