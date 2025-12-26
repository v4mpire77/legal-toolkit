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
from legal_toolkit.calendar import generate_cpr_ics
from legal_toolkit.audit import AuditGenerator

st.set_page_config(page_title="Legal Toolkit CLI/GUI", layout="wide")

def show_dashboard(user=None, auth=None):
    st.title("⚖️ Legal Toolkit: Professional Dashboard")
    st.markdown("### Civil Procedure Rules (CPR) Compliance Automation")
    
    db = None
    if auth and auth.client:
        db = DatabaseManager(auth.client)

    if user:
        with st.sidebar:
            st.divider()
            st.write(f"👤 **{user.user.email}**")
            if auth and st.button("Log Out", use_container_width=True):
                auth.sign_out()
                st.session_state['user'] = None
                st.rerun()

    # Sidebar for common settings
    st.sidebar.header("⚙️ Configuration")
    jurisdiction = st.sidebar.selectbox(
        "Jurisdiction",
        ['England & Wales', 'Scotland', 'Northern Ireland'],
        index=0
    )
    # Map friendly name back to internal ID if needed, or update logic
    jurisdiction_slug = jurisdiction.lower().replace(" & ", "-").replace(" ", "-")
    provider = BankHolidayProvider(jurisdiction_slug)

    # Tabs - Reordered for workflow priority
    tabs = st.tabs(["📅 CPR Deadlines", "📁 Bundle Generator", "💰 Issue Fees", "🤖 AI Assistant", "🗂️ Case Manager"])

    # --- TAB 1: DEADLINE CALCULATOR ---
    with tabs[0]:
        st.subheader("Procedural Deadline Calculator")
        st.info("Calculates deemed service and filing dates in accordance with CPR Part 6 and Part 15.")
        
        col1, col2 = st.columns([1, 1])
        
        # Initialize state for inputs if they don't exist
        if 'calc_date' not in st.session_state:
            st.session_state['calc_date'] = datetime.date.today()
        if 'calc_time' not in st.session_state:
            st.session_state['calc_time'] = datetime.time(12, 0)
        if 'extension_days' not in st.session_state:
            st.session_state['extension_days'] = 0
        
        with col1:
            st.markdown("#### 1. Date of Service")
            # Add a text input option for natural language dates
            use_natural_language = st.checkbox("Use natural language input", value=False, help="Type dates like 'next Monday' or '3 days ago'")
            
            if use_natural_language:
                date_text = st.text_input("Date (e.g., 'yesterday', '25 Dec')", value="today")
                try:
                    date_input = parse_date(date_text)
                except ValueError as e:
                    st.error(f"Invalid date format")
                    date_input = datetime.date.today()
            else:
                date_input = st.date_input("Date Document Sent", key="calc_date")
            
            time_input = st.time_input("Time Sent (24h)", key="calc_time")
            
            st.markdown("#### 2. Adjustments")
            extension_days = st.slider(
                "Agreed Extension (CPR 15.5)", 
                min_value=0, 
                max_value=28, 
                key="extension_days",
                help="Parties may agree to extend the period for filing a defense by up to 28 days."
            )
            
            sent_at = datetime.datetime.combine(date_input, time_input)
            
            if st.button("Calculate Deadlines", type="primary", use_container_width=True):
                deemed, deadline = calculate_deemed_service(sent_at, provider, extension_days=extension_days)
                
                st.divider()
                r1, r2 = st.columns(2)
                r1.metric("Deemed Service Date", deemed.strftime('%d %b %Y'), "CPR 6.14")
                r2.metric("Filing Deadline", deadline.strftime('%d %b %Y'), "CPR 15.4")
                
                if extension_days > 0:
                    st.caption(f"Includes {extension_days} day extension (CPR 15.5).")

                # --- CALENDAR EXPORT ---
                ics_data = generate_cpr_ics(sent_at, deemed, deadline)
                st.download_button(
                    label="📅 Add to Calendar (.ics)",
                    data=ics_data,
                    file_name="cpr_deadlines.ics",
                    mime="text/calendar",
                    use_container_width=True
                )

                # --- SAVE FUNCTIONALITY ---
                if user and db:
                    with st.expander("💾 Save Calculation to Case"):
                        case_ref = st.text_input("Client Reference / Matter No.", placeholder="e.g. MAT-001")
                        if st.button("Save Record"):
                            if case_ref:
                                data_payload = {
                                    "sent_at": sent_at.isoformat(),
                                    "deemed_service": deemed.isoformat(),
                                    "deadline": deadline.isoformat(),
                                    "jurisdiction": jurisdiction_slug,
                                    "extension_days": extension_days
                                }
                                db.save_case(user.user.id, case_ref, "deadline", data_payload)
                                st.toast("Calculation saved successfully!", icon="✅")
                            else:
                                st.error("Reference required.")

    # --- TAB 2: BUNDLE INDEXER & PDF ---
    with tabs[1]:
        st.subheader("eBundle Generator (PD 51O Compliant)")
        st.markdown("Generates a court-compliant PDF bundle with **Hyperlinked Index**, **Bates Stamping**, and **OCR text**.")
        
        bundle_col1, bundle_col2 = st.columns([2, 1])
        with bundle_col1:
            bundle_path = st.text_input("Source Directory", os.getcwd(), help="Absolute path to the folder containing your PDFs.")
            output_name = st.text_input("Output Filename", "Trial_Bundle_v1.pdf")
        with bundle_col2:
            bates_prefix = st.text_input("Bates Prefix", "BUNDLE")
            st.markdown("<br>", unsafe_allow_html=True) # Spacer
            if st.button("Generate Bundle", type="primary", use_container_width=True):
                if not os.path.exists(bundle_path):
                    st.error("Directory not found.")
                else:
                    engine = PDFEngine()
                    try:
                        with st.status("Processing Bundle...", expanded=True) as status:
                            st.write("🔍 Scanning documents...")
                            st.write("📑 Merging and generating Index...")
                            final_path = engine.generate_smart_bundle(bundle_path, output_name, bates_prefix)
                            status.update(label="Bundle Complete!", state="complete", expanded=False)
                        
                        st.success(f"Generated: `{final_path}`")
                    except Exception as e:
                        st.error(f"Generation Failed: {str(e)}")

    # --- TAB 3: FEE CALCULATOR ---
    with tabs[2]:
        st.subheader("Issue Fee Calculator")
        st.caption("Current Civil Proceedings Fees Order 2024")
        
        col1, col2 = st.columns(2)
        
        if 'claim_value' not in st.session_state:
            st.session_state['claim_value'] = 0.0

        with col1:
            claim_value = st.number_input(
                "Claim Value (£)", 
                min_value=0.0, 
                step=100.0, 
                format="%.2f",
                key="claim_value"
            )
            
            if st.button("Calculate Fee", use_container_width=True):
                fee = calculate_issue_fee(claim_value)
                st.metric(label="Court Fee Payable", value=f"£{fee:,.2f}")

                if user and db:
                    with st.expander("💾 Save Fee Assessment"):
                        fee_case_ref = st.text_input("Client Ref", key="fee_ref")
                        if st.button("Save Fee"):
                            if fee_case_ref:
                                db.save_case(user.user.id, fee_case_ref, "fee", {"claim_value": claim_value, "fee": fee})
                                st.toast("Fee saved!", icon="✅")
                            else:
                                st.error("Reference required.")
            
        with col2:
            st.info("Fees are calculated based on the money claim value including interest claimed.")

    # --- TAB 4: AI ASSISTANT ---
    with tabs[3]:
        st.subheader("AI Document Analysis")
        
        # Check environment variable to see if we are in Cloud Mode
        is_cloud = os.environ.get('STREAMLIT_RUNTIME') == 'cloud'

        col_cfg1, col_cfg2 = st.columns(2)
        with col_cfg1:
            ai_provider = st.radio("Processing Engine", ["Ollama (Local - Private)", "Gemini (Cloud - Fast)"], 
                                  index=1 if is_cloud else 0)
        
        provider_slug = "ollama" if "Ollama" in ai_provider else "gemini"
        
        # Import here to avoid circular dependencies
        from legal_toolkit.ai_assistant import AIAssistant
        ai = AIAssistant(provider=provider_slug)

        if provider_slug == "ollama" and is_cloud:
            st.warning("⚠️ **Ollama** is not available in Web Demo Mode. Please switch to Gemini.")
        elif provider_slug == "gemini" and not ai.is_available():
            st.warning("⚠️ **API Key Missing**: Set `GOOGLE_API_KEY` in secrets to enable Gemini.")
        else:
            status_col, _ = st.columns([1, 3])
            with status_col:
                if ai.is_available():
                    st.success(f"🟢 System Online")
                else:
                    st.error(f"🔴 System Offline")

            uploaded_file = st.file_uploader("Upload PDF (Particulars of Claim / Order)", type=['pdf'])
            
            if uploaded_file and ai.is_available():
                file_bytes = uploaded_file.read()
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("📝 Generate Summary", use_container_width=True):
                        with st.spinner("Analyzing legal context..."):
                            summary = ai.summarize_document(file_bytes, "summary")
                            st.markdown("### Case Summary")
                            st.write(summary)
                
                with c2:
                    if st.button("📅 Extract Dates", use_container_width=True):
                        with st.spinner("Scanning for procedural dates..."):
                            dates = ai.summarize_document(file_bytes, "dates")
                            st.markdown("### Critical Dates")
                            st.write(dates)

    # --- TAB 5: MY CASES ---
    with tabs[4]:
        st.subheader("Case Management")
        
        if not user:
            st.warning("Please Log In to access Case Management.")
        elif not db:
            st.error("Database connection unavailable.")
        else:
            cases = db.get_user_cases(user.user.id)
            if not cases:
                st.info("No active cases. Use the calculators to save your work.")
            else:
                for case in cases:
                    with st.expander(f"📂 {case['title']} ({case['case_type'].upper()})"):
                        c1, c2 = st.columns([3, 1])
                        with c1:
                             st.json(case['data'])
                        with c2:
                            # Audit Report Generator
                            audit_gen = AuditGenerator()
                            pdf_data = audit_gen.generate_report(case, user.user.email)
                            st.download_button(
                                "🖨️ Export Audit", 
                                data=pdf_data, 
                                file_name=f"Audit_{case['title']}.pdf", 
                                mime="application/pdf", 
                                key=f"audit_{case['id']}",
                                use_container_width=True
                            )

                            if st.button("🔄 Load", key=f"load_{case['id']}", use_container_width=True):
                                # Logic to populate session state based on case type
                                if case['case_type'] == "deadline":
                                    data = case['data']
                                    sent_at_dt = datetime.datetime.fromisoformat(data['sent_at'])
                                    st.session_state['calc_date'] = sent_at_dt.date()
                                    st.session_state['calc_time'] = sent_at_dt.time()
                                    st.session_state['extension_days'] = data.get('extension_days', 0)
                                    st.toast(f"Loaded {case['title']}", icon="📥")
                                
                                elif case['case_type'] == "fee":
                                    st.session_state['claim_value'] = float(case['data']['claim_value'])
                                    st.toast(f"Loaded {case['title']}", icon="📥")
                                    
                            if st.button("❌ Delete", key=f"del_{case['id']}", use_container_width=True):
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

