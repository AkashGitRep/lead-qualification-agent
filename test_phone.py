from hello_agent import normalize_phone


def test_plain_10_digits_accepted():
    assert normalize_phone("9876543210") == "9876543210"


def test_spaces_and_dashes_removed():
    assert normalize_phone("98765-43210") == "9876543210"
    assert normalize_phone("98765 43210") == "9876543210"


def test_plus91_prefix_stripped():
    assert normalize_phone("+91 98765 43210") == "9876543210"


def test_91_prefix_with_12_digits_stripped():
    assert normalize_phone("919876543210") == "9876543210"


def test_9_digits_rejected():
    assert normalize_phone("987654321") is None


def test_11_digits_rejected():
    assert normalize_phone("98765432100") is None


def test_letters_rejected():
    assert normalize_phone("98765abcde") is None


def test_empty_rejected():
    assert normalize_phone("") is None