# Research Findings: Legal Toolkit Optimization
**Date:** Monday, December 22, 2025

## 1. Robust Date Parsing
**Current State:** The project uses `datetime.strptime` which is fragile and requires exact format matching.
**Recommendation:** Integrate `dateparser`.
*   **Why:** It handles natural language ("25 Dec", "next Friday", "today") and multiple locales automatically.
*   **Benefit:** Reduces user error in the CLI and GUI when entering dates.

## 2. Advanced PDF Table Extraction
**Current State:** `PyMuPDF` (fitz) is used for text extraction, which flattens tables into unstructured text.
**Recommendation:** Integrate `pdfplumber` or `camelot-py`.
*   **Why:** Legal documents (schedules, bills of costs) often contain tables. `pdfplumber` preserves the grid structure, allowing us to extract data into Pandas DataFrames.
*   **Benefit:** Enables the AI Assistant to accurately query data from tables (e.g., "What is the total claim amount in the Schedule of Loss?").

## 3. CLI User Experience (UX)
**Current State:** `print()` statements for output.
**Recommendation:** Integrate `rich`.
*   **Why:** Provides beautiful formatting, color-coded logging, progress bars (for PDF merging), and tables for deadline results.
*   **Benefit:** Makes the tool feel like a professional product rather than a script.

## 4. Proposed Architecture Changes
*   **Refactor `deadlines.py`** to accept `dateparser` objects.
*   **New Module `legal_toolkit/tables.py`** using `pdfplumber`.
*   **Update `main.py`** to use `rich.console`.
