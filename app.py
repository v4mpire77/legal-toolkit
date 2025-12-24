"""
Legal Toolkit: Dashboard
Description: Streamlit-based graphical interface for legal automation.
"""

import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
import os
from legal_toolkit.holidays import BankHolidayProvider
from legal_toolkit.deadlines import calculate_deemed_service
from legal_toolkit.pdf_engine import PDFEngine
from legal_toolkit.utils import parse_date

st.set_page_config(page_title="Legal Toolkit CLI/GUI", layout="wide")

st.title("⚖️ Legal Toolkit: Professional Dashboard")
st.markdown("Automating compliance with the Civil Procedure Rules (England & Wales).")

# Sidebar for common settings
st.sidebar.header("Global Settings")
jurisdiction = st.sidebar.selectbox(
    "Jurisdiction",
    ['england-and-wales', 'scotland', 'northern-ireland'],
    index=0
)
provider = BankHolidayProvider(jurisdiction)

tabs = st.tabs(["📅 Deadline Calculator", "📁 Bundle Indexer & PDF", "🤖 AI Assistant (Beta)"])

# --- TAB 1: DEADLINE CALCULATOR ---
with tabs[0]:
    st.header("CPR Deadline Calculator")
    st.markdown("💡 **Tip**: You can enter dates like 'tomorrow', 'Friday', or '25 Dec 2024'")
    col1, col2 = st.columns(2)
    
    with col1:
        # Add a text input option for natural language dates
        use_natural_language = st.checkbox("Use natural language date input", value=False)
        
        if use_natural_language:
            date_text = st.text_input("Date of Transmission (e.g., 'tomorrow', 'Friday')", value="today")
            try:
                date_input = parse_date(date_text)
            except ValueError as e:
                st.error(f"Could not parse date: {e}")
                date_input = datetime.date.today()
        else:
            date_input = st.date_input("Date of Transmission", datetime.date.today())
        
        time_input = st.time_input("Time of Transmission", datetime.time(12, 0))
        
        sent_at = datetime.datetime.combine(date_input, time_input)
        
        if st.button("Calculate Deadlines"):
            deemed, deadline = calculate_deemed_service(sent_at, provider)
            
            st.success(f"**Deemed Service:** {deemed.strftime('%A, %d %B %Y')}")
            st.warning(f"**Filing Deadline:** {deadline.strftime('%A, %d %B %Y')}")
            
            # Data for Visualization
            vis_data = [
                dict(Task="Transmission", Start=sent_at, Finish=sent_at + datetime.timedelta(hours=1), Type="Actual"),
                dict(Task="Deemed Service", Start=deemed, Finish=deemed + datetime.timedelta(days=1), Type="Legal"),
                dict(Task="Filing Window", Start=deemed, Finish=deadline, Type="Period"),
                dict(Task="Deadline", Start=deadline, Finish=deadline + datetime.timedelta(hours=23), Type="Critical")
            ]
            df = pd.DataFrame(vis_data)
            fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Type", 
                             title="Procedural Timeline")
            fig.update_yaxes(autorange="reversed")
            st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: BUNDLE INDEXER & PDF ---
with tabs[1]:
    st.header("Smart Bundle Preparation")
    st.markdown("Combine multiple PDFs, add Bates Stamping, and generate a clickable Index.")
    
    bundle_path = st.text_input("Directory Path to PDF Documents", os.getcwd())
    bates_prefix = st.text_input("Bates Prefix", "BUNDLE")
    output_name = st.text_input("Output Filename", "COURT_BUNDLE_MASTER.pdf")
    
    if st.button("Generate Master Bundle"):
        if not os.path.exists(bundle_path):
            st.error("Directory not found.")
        else:
            engine = PDFEngine()
            with st.spinner("Processing documents..."):
                try:
                    final_path = engine.generate_smart_bundle(bundle_path, output_name, bates_prefix)
                    st.success(f"Bundle generated successfully: {final_path}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# --- TAB 3: AI ASSISTANT ---
with tabs[2]:
    st.header("Local AI Document Assistant")
    
    # Check environment variable to see if we are in Cloud Mode
    is_cloud = os.environ.get('STREAMLIT_RUNTIME') == 'cloud'

    if is_cloud:
        st.info("☁️ **Web Demo Mode**: Local AI features are disabled to protect server resources.")
        st.warning("To use the AI features (Llama3), please clone this repository and run it locally.")
    else:
        st.info("This feature uses a Local LLM (Ollama) to ensure client confidentiality remains on-device.")
        
        # Import here to avoid circular dependencies
        from legal_toolkit.ai_assistant import AIAssistant
        ai = AIAssistant(model_name="llama3")
        
        status_col, _ = st.columns([1, 3])
        with status_col:
            if ai.is_available():
                st.success("🟢 Ollama is Online")
            else:
                st.error("🔴 Ollama Offline")
                st.caption("Run `ollama serve` in a terminal.")

        uploaded_file = st.file_uploader("Upload a document for analysis", type=['pdf'])
        
        if uploaded_file and ai.is_available():
            file_bytes = uploaded_file.read()
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Summarize Particulars of Claim"):
                    with st.spinner("Analyzing document..."):
                        summary = ai.summarize_document(file_bytes, "summary")
                        st.markdown("### 📝 Case Summary")
                        st.write(summary)
            
            with col2:
                if st.button("Extract Key Dates"):
                    with st.spinner("Scanning for dates..."):
                        dates = ai.summarize_document(file_bytes, "dates")
                        st.markdown("### 📅 Critical Dates")
                        st.write(dates)
