from hello_agent import qualify


def lead(**overrides):
    base = {
        "property": "villa",
        "scope": "full",
        "budget": "10 to 20 lakh",
        "start": "within 1 month",
        "area": "whitefield",
    }
    base.update(overrides)
    return base


def test_valid_lead_qualifies():
    ok, reason = qualify(lead())
    assert ok is True
    assert reason == "qualified"


def test_under_10_lakh_rejected():
    ok, reason = qualify(lead(budget="under 10 lakh"))
    assert ok is False
    assert reason == "budget below minimum"


def test_later_start_rejected():
    ok, reason = qualify(lead(start="later"))
    assert ok is False
    assert reason == "start too far out"


def test_area_outside_bengaluru_rejected():
    ok, reason = qualify(lead(area="mumbai"))
    assert ok is False
    assert reason == "area not in service list"


def test_known_locality_accepted_case_insensitive():
    ok, _ = qualify(lead(area="Koramangala"))
    assert ok is True


def test_locality_with_extra_words_accepted():
    ok, _ = qualify(lead(area="near Whitefield main road"))
    assert ok is True