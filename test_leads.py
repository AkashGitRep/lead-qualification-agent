import json
import leads


def test_save_lead_creates_file(tmp_path, monkeypatch):
    monkeypatch.setattr(leads, "LEADS_FILE", tmp_path / "leads.json")
    leads.save_lead({"property": "villa", "area": "whitefield"}, "not_qualified")
    data = json.loads((tmp_path / "leads.json").read_text())
    assert len(data) == 1
    assert data[0]["status"] == "not_qualified"
    assert data[0]["area"] == "whitefield"
    assert "saved_at" in data[0]


def test_save_lead_appends_without_overwriting(tmp_path, monkeypatch):
    monkeypatch.setattr(leads, "LEADS_FILE", tmp_path / "leads.json")
    leads.save_lead({"area": "whitefield"}, "booked", "2026-11-18 12:00")
    leads.save_lead({"area": "koramangala"}, "not_qualified")
    data = json.loads((tmp_path / "leads.json").read_text())
    assert len(data) == 2
    assert data[0]["slot"] == "2026-11-18 12:00"
    assert data[1]["slot"] is None


def test_save_lead_keeps_status_and_slot(tmp_path, monkeypatch):
    monkeypatch.setattr(leads, "LEADS_FILE", tmp_path / "leads.json")
    leads.save_lead({"area": "whitefield"}, "qualified_not_booked", "2026-11-18 10:00")
    data = json.loads((tmp_path / "leads.json").read_text())
    assert data[0]["status"] == "qualified_not_booked"
    assert data[0]["slot"] == "2026-11-18 10:00"