import json
from datetime import datetime
from pathlib import Path

LEADS_FILE = Path("leads.json")

def save_lead(lead: dict, status: str, slot: str | None = None) -> None:
    """Append one lead record. status is 'booked', 'qualified_not_booked', or 'not_qualified'."""
    leads = json.loads(LEADS_FILE.read_text()) if LEADS_FILE.exists() else []
    leads.append({
        "saved_at": datetime.now().isoformat(timespec="seconds"),
        "status": status,
        "slot": slot,
        **lead,
    })
    LEADS_FILE.write_text(json.dumps(leads, indent=2))