# Legal Toolkit CLI

A unified command-line interface for automating legal workflows and ensuring compliance with the Civil Procedure Rules (CPR) in England & Wales.

## Overview

This project combines legal domain expertise with software engineering to solve practical problems faced by paralegals and solicitors. It currently includes tools for:

1.  **Court Bundle Indexing**: Automates the creation of indices and checks for compliance with **CPR Practice Direction 5B** regarding email size limits.
2.  **Deadline Calculation**: accurate computation of filing deadlines based on **CPR Part 10** and **CPR Part 2.8**.

## Features & Legal Basis

### 1. Bundle Indexer (`bundle`)
Generates a clean, formatted text index of all files in a directory and calculates total size.

*   **Legal Basis**:
    *   **CPR PD 5B para 2.1(1)**: Limits total email size to **25MB** for general/High Court filings.
    *   **CPR PD 5B para 2.1(2)**: Limits total email size to **10MB** for County Court filings.
*   **Functionality**:
    *   Detects file sizes.
    *   Warns if the bundle exceeds the specific limit for the chosen court.
    *   Generates an `INDEX.txt` ready for inclusion in correspondence.

### 2. Deadline Calculator (`deadline`)
Calculates the 14-day deadline for filing an Acknowledgment of Service or Defence.

*   **Legal Basis**:
    *   **CPR 10.3(1)(b)**: The period for filing an acknowledgment of service is 14 days after service of the claim form.
    *   **CPR 2.8(5)**: If a deadline ends on a day the court office is closed (Saturday, Sunday, or Bank Holiday), the act is done in time if done on the next day the court office is open.
*   **Functionality**:
    *   Takes a Service Date.
    *   Adds 14 days.
    *   Automatically adjusts for weekends (Next Working Day rule).

## Usage

### Prerequisites
*   Python 3.x

### Installation
Clone the repository:
```bash
git clone https://github.com/yourusername/legal-toolkit.git
cd legal-toolkit
```

### Commands

**1. Calculate a Deadline**
```bash
python -m legal_toolkit.main deadline --date 2025-12-20
```

**2. Index a Bundle (General/High Court - 25MB)**
```bash
python -m legal_toolkit.main bundle --path ./my_case_documents
```

**3. Index a Bundle (County Court - 10MB)**
```bash
python -m legal_toolkit.main bundle --path ./county_court_docs --court county
```

## Disclaimer
This software is designed to assist legal professionals but does not constitute legal advice. While efforts are made to ensure accuracy with current Civil Procedure Rules (as of 2025), users should always verify deadlines and compliance requirements against the official [Justice.gov.uk](https://www.justice.gov.uk/courts/procedure-rules/civil) rules, particularly regarding Bank Holidays which are not currently automated.
