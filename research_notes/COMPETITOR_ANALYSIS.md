# Legal Tech Competitor Analysis (2025)

## 1. Market Leaders Overview

### **Clio**
- **Target:** Mid-to-Large Firms.
- **Killer Feature:** "Clio ecosystem" (Manage, Grow, Draft, Work) - seamless integration.
- **2025 Focus:** AI-powered drafting & "Clio Duo" (AI assistant).
- **Weakness:** Premium pricing; complex for solo practitioners.

### **MyCase**
- **Target:** Small-to-Mid Firms.
- **Killer Feature:** Client Portal & Communication (Texting/Chat).
- **2025 Focus:** "Billables AI" (auto-time tracking) & Predictive Calendars.
- **Weakness:** UI considered less modern than PracticePanther.

### **PracticePanther**
- **Target:** Solo to Mid-sized.
- **Killer Feature:** Automation Workflows & "PantherPayments".
- **2025 Focus:** E-Signature Templates & Visual Customization.
- **Weakness:** Some core features require paid add-ons.

---

## 2. Feature Gap Analysis (Our Opportunities)

| Feature Category | Competitor Standard | Our "Legal Toolkit" Edge |
| :--- | :--- | :--- |
| **Deadlines** | Rules-based (LawToolBox integration). | **Local-First & Instant.** No subscription needed for basic CPR calc. |
| **Bundling** | Cloud-based, re-pagination is slow/online. | **Offline Engine.** Drag-and-drop re-ordering instantly on-device. |
| **AI Analysis** | "Black Box" summaries. | **Cited Summaries.** AI output linked to specific PDF page numbers. |
| **Data Privacy** | Cloud-storage mandatory. | **Local-Storage Option.** Process sensitive PDFs without upload. |
| **Integration** | Deep API links (Outlook/Gmail). | **Simple .ICS Export.** Universal calendar file generation. |

## 3. Recommended "Phase 2" Roadmap

1.  **Calendar Export (.ics):**
    *   *Why:* Solves "Integration Fatigue" without complex API dev.
    *   *Dev Effort:* Low.

2.  **Smart Bundle Re-ordering:**
    *   *Why:* Direct hit on competitor weakness (clunky online editors).
    *   *Dev Effort:* Medium (needs new Streamlit UI component).

3.  **"Cited" AI Summaries:**
    *   *Why:* Builds trust in AI (Competitors like CoCounsel are expensive).
    *   *Dev Effort:* High (requires modifying `pdf_engine` to map text->pages).

4.  **Client Portal Lite (via Streamlit):**
    *   *Why:* Mimic MyCase's best feature using Supabase Auth.
    *   *Dev Effort:* Medium.
