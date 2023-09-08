from parser.services.utils import extract_number, extract_urls


def test_extract_urls():
    assert extract_urls("1\n2\n3\n") == ["1", "2", "3"]


def test_extract_number():
    assert extract_number(" 1 2 3") == 123
    assert extract_number("dsadsa 12000 dsadsa") == 12000
    assert extract_number("12.01") == 12.01
    assert extract_number("12,01") == 12.01
