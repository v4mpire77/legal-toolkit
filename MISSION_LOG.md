# 🤖 MISSION RESUME: LEGAL TOOLKIT

## 📝 URGENT TODO
- [ ] **Google AI Key:** Generate key at [AI Studio](https://aistudio.google.com/) and add to Streamlit Secrets as `GOOGLE_API_KEY`.

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
- **Goal:** [COMPLETED] Added a button to download an `.ics` file for calculated deadlines using the `ics` library.
- **Library added:** `ics`.

## 🤖 HYBRID AI ASSISTANT (GEMINI + OLLAMA)
- **Goal:** [COMPLETED] Enable AI features on Streamlit Cloud using Google Gemini API (Free Tier).
- **Logic:** App now toggles between Ollama (Local/Private) and Gemini (Cloud/Public).
- **Action Required:** User needs to generate a `GOOGLE_API_KEY` at [AI Studio](https://aistudio.google.com/) and add it to secrets.

## 📂 KEY FILES
- `app.py`: Main UI and Tab logic.
- `legal_toolkit/auth.py`: Supabase & Google login logic.
- `research_notes/`: Market research and strategy docs.

**Note to self:** Start by fixing the 403 Iframe bug in `app.py` before moving to the Calendar feature.
