# ⚖️ Legal Toolkit (v2.0) - Legal Engineering Edition

A professional-grade Python suite for automating UK legal workflows. This project demonstrates **Legal Engineering**: the intersection of rigorous procedural law (Civil Procedure Rules) and advanced software architecture.

## 🚀 Key Features

### 1. 🧠 Algorithmic Law: CPR Compliance
The toolkit encodes complex procedural logic from the **Civil Procedure Rules (CPR)**:
*   **Deemed Service (CPR 6.14 & 6.26)**: Calculates the exact date of service for Claim Forms, accounting for the **4:30 PM electronic cutoff** and the "second business day" rule.
*   **Resilient Holiday Provider**: Integrates the **GOV.UK Bank Holiday API** with a cache-first, offline-ready architecture. It supports distinct rules for England & Wales, Scotland, and Northern Ireland.
*   **Procedural Timeline**: Visualizes the gap between transmission and deemed service using interactive Gantt charts (via Plotly).

### 2. 📄 High-Performance Document Engineering
Built on **PyMuPDF**, the toolkit automates the preparation of court-compliant electronic bundles (Practice Direction 5B):
*   **Automated Bates Stamping**: Applies sequential, formatted numbering to the footer of thousands of pages in seconds.
*   **Clickable TOC Generation**: Automatically creates a nested, navigable Table of Contents (Bookmarks) based on document structure.
*   **Smart Merging**: Combines heterogeneous PDFs into a single litigation master file without losing metadata.

### 3. 📊 Visual Dashboard (Streamlit)
A modern, web-based interface for non-technical legal professionals ("fee earners"), featuring interactive visualizations and drag-and-drop bundle generation.

## 🛠️ Tech Stack
*   **Language**: Python 3.12+
*   **PDF Engine**: PyMuPDF (C-backed for speed)
*   **UI Framework**: Streamlit
*   **Data Viz**: Plotly Express, Pandas
*   **API/Networking**: Requests (with Resilient Provider Pattern)

## 📦 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/v4mpire77/legal-toolkit.git
   cd legal-toolkit
   ```

2. **Set up Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the Dashboard**:
   ```bash
   streamlit run app.py
   ```

4. **Run via CLI**:
   ```bash
   python3 -m legal_toolkit.main deadline --date 2024-12-20 --time 17:00
   ```

## ⚖️ Legal Disclaimer
This software is for educational and professional assistance only and does not constitute legal advice. While it implements CPR rules (including the 4:30 PM cutoff), always cross-reference with official [Justice.gov.uk](https://www.justice.gov.uk) documentation.

