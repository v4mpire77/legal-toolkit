from ics import Calendar, Event
import datetime

def generate_cpr_ics(sent_at, deemed, deadline):
    """
    Generates an .ics file content for CPR deadlines.
    """
    c = Calendar()

    # Event 1: Transmission
    e_sent = Event()
    e_sent.name = "📄 CPR: Document Transmission"
    e_sent.begin = sent_at
    e_sent.description = "Document sent/transmitted via electronic means or post."
    c.events.add(e_sent)

    # Event 2: Deemed Service
    e_deemed = Event()
    e_deemed.name = "✅ CPR: Deemed Service"
    e_deemed.begin = deemed
    e_deemed.description = "The date the document is legally deemed served under CPR rules."
    c.events.add(e_deemed)

    # Event 3: Filing Deadline
    e_deadline = Event()
    e_deadline.name = "🚨 CPR FILING DEADLINE"
    # Set as an all-day event for the deadline date
    e_deadline.begin = deadline
    e_deadline.make_all_day()
    e_deadline.description = "CRITICAL: Final date for filing response or next step."
    c.events.add(e_deadline)

    return c.serialize()
