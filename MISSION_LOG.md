# 🤖 MISSION RESUME: LEGAL TOOLKIT

## 📍 CURRENT STATUS
- **Deployment:** Live on [legal-toolkit.streamlit.app](https://legal-toolkit.streamlit.app/)
- **Infrastructure:** Supabase Auth & DB are 100% configured (Email/Pass works).
- **GitHub:** Main branch is up-to-date.

## 🛠️ THE "BIG BUG" (GOOGLE AUTH 403)
- **Problem:** Clicking "Sign in with Google" gives a 403 error on Streamlit Cloud.
- **Diagnosis:** We are using `<meta refresh>` to redirect. Streamlit Cloud runs in an **iframe**, and Google blocks OAuth requests from iframes (clickjacking protection).
- **The Fix:** [FIXED] Replaced `st.button` + meta refresh with a direct `<a>` tag using `target="_top"`.

## 🚀 NEXT FEATURE: CALENDAR EXPORT
- **Spec:** `research_notes/NEXT_STEPS_CALENDAR.md`
- **Goal:** Add a button to download an `.ics` file for calculated deadlines.
- **Library needed:** `pip install ics`.

## 📂 KEY FILES
- `app.py`: Main UI and Tab logic.
- `legal_toolkit/auth.py`: Supabase & Google login logic.
- `research_notes/`: Market research and strategy docs.

**Note to self:** Start by fixing the 403 Iframe bug in `app.py` before moving to the Calendar feature.
