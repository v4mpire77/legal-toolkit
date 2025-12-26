"""
Legal Toolkit: Dashboard
Description: Streamlit-based graphical interface for legal automation.
"""

import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
import os
import json
from legal_toolkit.holidays import BankHolidayProvider
from legal_toolkit.deadlines import calculate_deemed_service
from legal_toolkit.pdf_engine import PDFEngine
from legal_toolkit.utils import parse_date
from legal_toolkit.fees import calculate_issue_fee
from legal_toolkit.auth import AuthManager
from legal_toolkit.db import DatabaseManager

st.set_page_config(page_title="Legal Toolkit CLI/GUI", layout="wide")

def show_dashboard(user=None, auth=None):
    st.title("⚖️ Legal Toolkit: Professional Dashboard")
    
    db = None
    if auth and auth.client:
        db = DatabaseManager(auth.client)

    if user:
        st.caption(f"Logged in as: {user.user.email}")
        if auth and st.sidebar.button("Log Out"):
            auth.sign_out()
            st.session_state['user'] = None
            st.rerun()

    st.markdown("Automating compliance with the Civil Procedure Rules (England & Wales).")

    # Sidebar for common settings
    st.sidebar.header("Global Settings")
    jurisdiction = st.sidebar.selectbox(
        "Jurisdiction",
        ['england-and-wales', 'scotland', 'northern-ireland'],
        index=0
    )
    provider = BankHolidayProvider(jurisdiction)

    tabs = st.tabs(["📅 Deadline Calculator", "📁 Bundle Indexer & PDF", "🤖 AI Assistant (Beta)", "💰 Fee Calculator", "🗂️ My Cases"])

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

                # --- SAVE FUNCTIONALITY ---
                if user and db:
                    st.markdown("---")
                    with st.expander("💾 Save this Calculation"):
                        case_ref = st.text_input("Case Reference / Title", placeholder="e.g. Smith v Jones")
                        if st.button("Save to Profile"):
                            if case_ref:
                                data_payload = {
                                    "sent_at": sent_at.isoformat(),
                                    "deemed_service": deemed.isoformat(),
                                    "deadline": deadline.isoformat(),
                                    "jurisdiction": jurisdiction
                                }
                                db.save_case(user.user.id, case_ref, "deadline", data_payload)
                                st.success("Saved to profile!")
                            else:
                                st.error("Please enter a Case Reference.")

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

    # --- TAB 4: FEE CALCULATOR ---
    with tabs[3]:
        st.header("Court Issue Fee Calculator")
        st.markdown("Calculates the issue fee for Money Claims (Form EX50).")
        
        col1, col2 = st.columns(2)
        
        with col1:
            claim_value = st.number_input(
                "Value of your Claim (£)", 
                min_value=0.0, 
                step=100.0, 
                format="%.2f"
            )
            
            if st.button("Calculate Fee"):
                fee = calculate_issue_fee(claim_value)
                st.metric(label="Court Fee to Pay", value=fee)

                # --- SAVE FUNCTIONALITY ---
                if user and db:
                    st.markdown("---")
                    with st.expander("💾 Save Fee Calculation"):
                        fee_case_ref = st.text_input("Case Reference", placeholder="e.g. Smith Debt", key="fee_ref")
                        if st.button("Save Fee"):
                            if fee_case_ref:
                                db.save_case(user.user.id, fee_case_ref, "fee", {"claim_value": claim_value, "fee": fee})
                                st.success("Saved to profile!")
                            else:
                                st.error("Please enter a Case Reference.")
            
        with col2:
            st.info(
                """
                **Fee Brackets (simplified):**
                * Up to £300: **£35**
                * £300 - £500: **£50**
                * £5k - £10k: **£455**
                * Over £10k: **5% of claim**
                * Over £200k: **£10,000 (Cap)**
                """
            )

    # --- TAB 5: MY CASES ---
    with tabs[4]:
        st.header("🗂️ My Cases & Saved Data")
        
        if not user:
            st.warning("Please Log In to view your saved cases.")
        elif not db:
            st.error("Database connection unavailable.")
        else:
            cases = db.get_user_cases(user.user.id)
            if not cases:
                st.info("No saved cases found. Go to other tabs to save your work!")
            else:
                for case in cases:
                    with st.expander(f"{case['title']} ({case['case_type'].upper()}) - {parse_date(case['created_at']).strftime('%d %b %Y')}"):
                        st.json(case['data'])
                        if st.button("Delete Case", key=f"del_{case['id']}"):
                            db.delete_case(case['id'])
                            st.rerun()

# --- MAIN EXECUTION ---
auth = AuthManager()

if not auth.is_configured():
    st.sidebar.warning("⚠️ Supabase not configured. Running in Guest Mode.")
    st.sidebar.markdown("To enable Login, set `SUPABASE_URL` and `SUPABASE_KEY` in environment variables or `.streamlit/secrets.toml`.")
    show_dashboard()
else:
    # Initialize session state for user
    if 'user' not in st.session_state:
        # Try to get existing session from Supabase client
        try:
            session = auth.client.auth.get_session()
            if session:
                st.session_state['user'] = session
            else:
                st.session_state['user'] = None
        except:
            st.session_state['user'] = None

    # If user is logged in
    if st.session_state['user']:
        show_dashboard(st.session_state['user'], auth)
    else:
        # Show Login/Signup
        st.title("🔐 Welcome to Legal Toolkit")
        
        login_tab, signup_tab = st.tabs(["Login", "Sign Up"])
        
        with login_tab:
            st.header("Sign In")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Login", use_container_width=True):
                    res = auth.sign_in(email, password)
                    if res and res.user:
                        st.session_state['user'] = res
                        st.success("Logged in successfully!")
                        st.rerun()
            with col2:
                # Google OAuth - Direct Link to avoid 403 Iframe Error
                # We pre-fetch the URL and render it as a standard HTML link with target="_top"
                oauth_res = auth.sign_in_with_google()
                if oauth_res and hasattr(oauth_res, 'url'):
                    st.markdown(
                        f'''
                        <a href="{oauth_res.url}" target="_top" style="
                            display: inline-block;
                            width: 100%;
                            padding: 0.5rem;
                            color: #31333F;
                            background-color: #FFFFFF;
                            border: 1px solid rgba(49, 51, 63, 0.2);
                            border-radius: 0.5rem;
                            text-align: center;
                            text-decoration: none;
                            font-weight: 400;
                            margin-top: 2px;
                        ">
                            🚀 Sign in with Google
                        </a>
                        ''',
                        unsafe_allow_html=True
                    )
        
        with signup_tab:
            st.header("Create Account")
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Password", type="password", key="signup_pass")
            if st.button("Sign Up"):
                res = auth.sign_up(new_email, new_password)
                if res and res.user:
                    st.success("Account created! You can now log in.")

