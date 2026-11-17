import json
from datetime import datetime, timedelta
from pathlib import Path

BOOKINGS_FILE = Path("bookings.json")
BUSINESS_HOURS = range(10, 18)  # 10:00 to 17:00 start times

def get_available_slots(days_ahead: int = 3) -> list[str]:
    """Mock calendar: returns the next free slots during business hours."""
    slots = []
    start = datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(days=1)
    for day in range(days_ahead):
        date = start + timedelta(days=day)
        for hour in BUSINESS_HOURS:
            slot = date.replace(hour=hour)
            if slot.weekday() < 6:  # Monday to Saturday
                slots.append(slot.strftime("%Y-%m-%d %H:%M"))
    return slots[:6]

def _load() -> list[dict]:
    if BOOKINGS_FILE.exists():
        return json.loads(BOOKINGS_FILE.read_text())
    return []

def book_slot(phone: str, name: str, slot: str) -> tuple[bool, str]:
    if slot not in get_available_slots():
        return False, "slot not available"
    bookings = _load()
    if any(b["phone"] == phone for b in bookings):
        return False, "this contact already has a booking"  # idempotency
    if any(b["slot"] == slot for b in bookings):
        return False, "slot already taken"
    bookings.append({"phone": phone, "name": name, "slot": slot})
    BOOKINGS_FILE.write_text(json.dumps(bookings, indent=2))
    return True, "booked"