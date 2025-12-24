# ⚖️ Legal Toolkit (v3.0) - Legal Engineering Edition

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://share.streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A professional-grade Python suite for automating UK legal workflows. This project demonstrates **Legal Engineering**: the intersection of rigorous procedural law (Civil Procedure Rules) and advanced software architecture.

## 🚀 Key Features

### 1. 🧠 Algorithmic Law: CPR Compliance
The toolkit encodes complex procedural logic from the **Civil Procedure Rules (CPR)**:
*   **Deemed Service (CPR 6.14 & 6.26)**: Calculates the exact date of service for Claim Forms, accounting for the **4:30 PM electronic cutoff** and the "second business day" rule.
*   **Natural Language Input**: Parse dates like "tomorrow", "next Friday", or "25 Dec 2025" automatically.
*   **Resilient Holiday Provider**: Integrates the **GOV.UK Bank Holiday API** with a cache-first, offline-ready architecture.

### 2. 💰 Court Fee Calculator (Form EX50)
*   **Instant Calculation**: Automatically calculates Issue Fees for Money Claims.
*   **Complex Logic**: Handles all fee brackets, the "5% rule" for claims between £10k-£200k, and the £10,000 cap.

### 3. 📄 High-Performance Document Engineering
Built on **PyMuPDF** and **pdfplumber**, the toolkit automates bundle preparation:
*   **Smart Table Extraction**: Uses AI to identify and extract financial tables (e.g., Schedules of Loss) from PDFs into CSV format.
*   **Automated Bates Stamping**: Applies sequential, formatted numbering to thousands of pages in seconds.
*   **Clickable TOC Generation**: Automatically creates a nested, navigable Table of Contents.

### 4. 🤖 Privacy-First AI Assistant
*   **Local LLM Integration**: Uses **Ollama (Llama 3)** to summarize legal documents locally.
*   **Cloud-Safe Architecture**: Features "Lazy Importing" to ensure the app runs smoothly on the cloud (in read-only mode) while offering powerful AI features on local machines.
*   **Data Security**: No client data ever leaves the device.

## 🛠️ Tech Stack
*   **Language**: Python 3.12+
*   **Web Framework**: Streamlit
*   **PDF Engine**: PyMuPDF, pdfplumber
*   **AI/LLM**: Ollama, Llama 3
*   **Testing**: unittest, pytest
*   **CLI**: Rich (for beautiful terminal output)

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
   python3 -m legal_toolkit.main deadline --date "tomorrow" --time 16:45
   ```

## 🧪 Testing

The project maintains high reliability with a comprehensive test suite.

```bash
# Run all tests
python3 -m unittest discover tests
```

## ⚖️ Legal Disclaimer
This software is for educational and professional assistance only and does not constitute legal advice. While it implements CPR rules (including the 4:30 PM cutoff), always cross-reference with official [Justice.gov.uk](https://www.justice.gov.uk) documentation.