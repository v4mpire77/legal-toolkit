# ⚖️ Legal Tech Compliance Dashboard

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-FF4B4B)
![Status](https://img.shields.io/badge/Maintenance-Active-green)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modular Legal Technology toolkit designed to automate **Civil Procedure Rules (CPR)** compliance, document bundling, and court fee calculations. 

A professional-grade Python suite demonstrating **Legal Engineering**: the intersection of rigorous procedural law and advanced software architecture.

## 🌟 Key Features

### 1. 📅 Procedural Deadline Engine
- **CPR 6.14 & 6.26 Logic:** Automatically calculates "Deemed Service" dates, accounting for the 4:30 PM rule and weekends.
- **Natural Language Aware:** Automatically parse dates like "tomorrow", "next Friday", or "25 Dec 2025".
- **Bank Holiday Aware:** Integrated UK Bank Holiday API (cache-first) to skip non-business days across England & Wales, Scotland, and Northern Ireland.
- **Visual Timeline:** Generates interactive Gantt charts (via Plotly) for case management.

### 2. 💰 Court Fee Calculator (Form EX50)
- **HMCTS Automation:** Instantly calculates issue fees for Money Claims based on Form EX50.
- **Dynamic Logic:** Handles the "5% Rule" for claims between £10k-£200k and applies the £10,000 cap automatically.

### 3. 🤖 Privacy-First AI Assistant
- **"Cloud Proof" Architecture:** 
  - *Local Mode:* Uses **Ollama (Llama 3)** to summarize confidential PDFs and extract key dates on-device (GDPR compliant).
  - *Cloud Mode:* Gracefully degrades to standard features when hosted online to prevent crashes via "Lazy Importing".
- **Smart Table Extraction:** Integrates **pdfplumber** to identify and extract financial tables (e.g., Schedules of Loss) into structured context for the AI.

### 4. 📁 Bundle Automation
- **PDF Engine:** Automates Bates Stamping, clickable TOC (Bookmark) generation, and smart merging of court bundles (Practice Direction 5B).

### 5. 🔐 Authentication & Data Persistence (New)
- **Supabase Integration:** Secure Sign-up, Login, and Data Storage using Supabase (PostgreSQL).
- **Cloud Sync:** Save your deadline calculations and fee estimates to your personal "Case File" and access them anywhere.
- **Guest Mode:** The app works fully without login, but data will not be saved.

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Core Logic:** Python 3.12+ (pandas, pdfplumber, fitz, rich)
- **Database/Auth:** Supabase
- **AI/LLM:** Ollama (Llama 3)
- **Testing:** `unittest` & `pytest`
- **Documentation:** Auto-generated via `pdoc`

## 🚀 Quick Start (Local)

1. **Clone the repo**
   ```bash
   git clone https://github.com/v4mpire77/legal-toolkit.git
   cd legal-toolkit
   ```

2. **Install Dependencies**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Database (Optional)**
   To enable User Accounts and Saving:
   - Create a free project at [Supabase](https://supabase.com).
   - Go to the SQL Editor and run the contents of `SUPABASE_SCHEMA.sql` to set up the tables and security policies.
   - Copy your `Project URL` and `anon public key` from Project Settings > API.
   - Create a `.streamlit/secrets.toml` file:
     ```toml
     SUPABASE_URL = "your-project-url"
     SUPABASE_KEY = "your-anon-key"
     ```
   *(If skipped, the app will run in Guest Mode).*

4. **Run the App**
   ```bash
   streamlit run app.py
   ```

## 🧪 Running Tests

To verify the legal logic (Deemed Service and Fees):

```bash
python3 -m unittest discover tests
```

---

*Disclaimer: This tool provides guidance based on CPR rules but does not constitute legal advice. Always cross-check with the official [Justice.gov.uk](https://www.justice.gov.uk) documentation.*
