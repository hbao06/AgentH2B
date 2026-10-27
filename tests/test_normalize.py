from datamate.normalize import normalize_answer, normalize_string


def test_string_keeps_vietnamese_diacritics_and_normalizes_punctuation():
    assert normalize_string("  Cà-phê sữa  ") == "cà phê sữa"


def test_number_and_percent_rounding():
    assert normalize_answer("number", 12.0) == 12
    assert normalize_answer("percent", 12.345) == 12.35
