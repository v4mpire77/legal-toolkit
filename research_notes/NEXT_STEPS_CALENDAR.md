# Feature Spec: Calendar Export (.ics)

## 🎯 Objective
Enable users to export calculated CPR deadlines directly to Microsoft Outlook, Apple Calendar, or Google Calendar using a standard `.ics` file.

## 🛠️ Technical Plan
1. **Dependency:** Add `ics` to `requirements.txt`.
2. **Logic:** 
   - Create a helper in `legal_toolkit/utils.py` or a new `legal_toolkit/calendar.py`.
   - Function `generate_cpr_ics(sent_at, deemed, deadline)`:
     - Event 1: **Transmission** (sent_at).
     - Event 2: **Deemed Service** (deemed).
     - Event 3: **🚨 CPR Filing Deadline** (deadline) - set as an All-Day event with a 15-minute "High Priority" reminder.
3. **UI Integration:**
   - In `app.py` (Tab 1), add `st.download_button` after a successful calculation.
   - Label: "📅 Export to Outlook/iCal".

## 🚀 Execution Script (for next time)
```python
from ics import Calendar, Event
import streamlit as st

c = Calendar()
e = Event()
e.name = "🚨 CPR Filing Deadline"
e.begin = deadline_date
c.events.add(e)

st.download_button("Download Calendar File", str(c), "deadline.ics")
```

---
*Notes: This solves the "Integration Fatigue" pain point identified in Phase 1 research.*
