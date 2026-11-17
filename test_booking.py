import booking


def test_slots_are_in_business_hours():
    for s in booking.get_available_slots():
        hour = int(s[-5:-3])
        assert 10 <= hour <= 17


def test_double_booking_same_slot_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(booking, "BOOKINGS_FILE", tmp_path / "b.json")
    slot = booking.get_available_slots()[0]
    assert booking.book_slot("9999", "A", slot)[0] is True
    assert booking.book_slot("8888", "B", slot)[0] is False


def test_same_contact_cannot_book_twice(tmp_path, monkeypatch):
    monkeypatch.setattr(booking, "BOOKINGS_FILE", tmp_path / "b.json")
    slots = booking.get_available_slots()
    assert booking.book_slot("9999", "A", slots[0])[0] is True
    ok, reason = booking.book_slot("9999", "A", slots[1])
    assert ok is False
    assert "already" in reason