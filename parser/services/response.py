from dataclasses import dataclass
import logging

from parser.models import SiteParseSettings
from jsonpath_ng import parse
from lxml import html

log = logging.getLogger(__name__)


@dataclass
class ParseResult:
    title: str | None = None
    price: int | float | None = None


def process_css(settings: SiteParseSettings, res: str, multiple: bool = False):
    """Process css using lxml"""
    tree = html.fromstring(res)

    path_title = settings.path_title
    path_price = settings.path_price

    res_title = tree.cssselect(path_title)
    res_price = tree.cssselect(path_price)

    res: list[ParseResult] = []
    log.debug(f"CSS Process result: {res_title} | {res_price}")

    for title, price in zip(res_title, res_price):
        res.append(ParseResult(title=title, price=price))

    return res


def process_json(settings: SiteParseSettings, res: dict, multiple: bool = False) -> list[ParseResult]:
    """Process json using jsonpath"""

    path_title = parse(settings.path_title)
    path_price = parse(settings.path_price)

    res_title = path_title.find(res)
    res_price = path_price.find(res)

    res: list[ParseResult] = []

    for title, price in zip(res_title, res_price):
        res.append(ParseResult(title=title.value, price=price.value))

    return res


def parse_result(settings: SiteParseSettings, res: str | dict, multiple: bool = False):
    """Parse request result"""

    if isinstance(res, dict):
        return process_json(settings, res, multiple=multiple)
    else:
        return process_css(settings, res, multiple=multiple)
