from dataclasses import dataclass
import logging

from parser.models import ParseTask, SiteParseSettings
from jsonpath_ng import parse
from lxml import html

from parser.services.utils import extract_number

log = logging.getLogger(__name__)


@dataclass
class ParseResult:
    title: str
    price: float


def process_css(settings: SiteParseSettings, res: str, task: ParseTask, multiple: bool = False):
    """Process css using lxml"""
    tree = html.fromstring(res)

    path_title = settings.path_title
    path_price = settings.path_price

    res_title: str = tree.cssselect(path_title)
    res_price: str = tree.cssselect(path_price)

    res: list[ParseResult] = []
    log.debug(f"CSS Process result: {res_title} | {res_price}")

    for title, price in zip(res_title, res_price):
        try:
            res.append(ParseResult(title=title.text, price=extract_number(price.text)))
        except Exception as e:
            task.log.error("CSS row processing error", exc_info=e)

    return res


def process_json(settings: SiteParseSettings, res: dict, task: ParseTask, multiple: bool = False) -> list[ParseResult]:
    """Process json using jsonpath"""

    path_title = parse(settings.path_title)
    path_price = parse(settings.path_price)

    res_title = path_title.find(res)
    res_price = path_price.find(res)

    res: list[ParseResult] = []

    for title, price in zip(res_title, res_price):
        try:
            res.append(ParseResult(title=title.value, price=extract_number(price.value)))
        except Exception as e:
            task.log.error("JSON row processing error", exc_info=e)

    return res


def parse_result(settings: SiteParseSettings, res: str | dict, task: ParseTask, multiple: bool = False):
    """Parse request result"""

    if isinstance(res, dict):
        return process_json(settings, res, task, multiple=multiple)
    else:
        return process_css(settings, res, task, multiple=multiple)
