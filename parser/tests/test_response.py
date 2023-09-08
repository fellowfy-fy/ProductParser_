import pytest
from parser.services import response
from parser.tests.factories.parse_settings import SiteParseSettingsFactory


@pytest.mark.unittest
def test_process_css():
    inp = """
<div class="product">
    <h4>Product1</h4>
    <span>100</span>
</div>
<div class="product">
    <h4>Product2</h4>
    <span>200</span>
</div>
"""
    settings = SiteParseSettingsFactory.build(path_title=".product h4", path_price=".product span")

    res = response.process_css(settings, inp, multiple=True)
    assert res == [
        response.ParseResult(title="Product1", price=100),
        response.ParseResult(title="Product2", price=200),
    ]


@pytest.mark.unittest
def test_process_json():
    inp = {
        "products": [
            {
                "title": "Product1",
                "price": 100,
            },
            {
                "title": "Product2",
                "price": 200,
            },
        ]
    }
    settings = SiteParseSettingsFactory.build(path_title="$.products[*].title", path_price="$.products[*].title")
    res = response.process_json(settings, inp, multiple=True)
    assert res == [
        response.ParseResult(title="Product1", price=100),
        response.ParseResult(title="Product2", price=200),
    ]
