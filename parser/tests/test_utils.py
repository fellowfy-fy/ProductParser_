from parser.services.utils import extract_number, extract_urls, select_best_settings, url_regex
from parser.tests.factories.parse_settings import SiteParseSettingsFactory


def test_extract_urls():
    assert extract_urls("1\n2\n3\n") == ["1", "2", "3"]


def test_extract_number():
    # assert extract_number(" 1 2 3") == 123
    assert extract_number("dsadsa 12000 dsadsa") == 12000
    assert extract_number("12.01") == 12.01
    assert extract_number("12,01") == 12.01
    assert extract_number("615 руб/м2") == 615
    assert extract_number("2 100") == 2100
    assert extract_number("2 419 руб.") == 2419


def test_select_best_settings():
    s1 = SiteParseSettingsFactory.build(url="https://example.com/1/2/3")
    s2 = SiteParseSettingsFactory.build(url="https://example.com/1/2")
    s3 = SiteParseSettingsFactory.build(url="https://example2.com/1/2")
    settings = [s1, s2, s3]

    assert select_best_settings("https://example.com/1/2/3/4", settings)[0] == s1
    assert select_best_settings("https://example.com", settings)[0] == s2
    assert select_best_settings("https://example.com/1/2", settings)[0] == s2
    assert select_best_settings("https://example2.com/1/2", settings)[0] == s3


def test_url_regex():
    assert (
        url_regex(
            r"\/product\/[\w-]*(\d{8})\/",
            "https://leroymerlin.ru/product/fasadnaya-panel-docke-dacha-kirpich-gladkiy-temno-korichnevyy-046-m-82402506/",
            "http://example.com/?prodictID={0}",
        )
        == "http://example.com/?prodictID=82402506"
    )
