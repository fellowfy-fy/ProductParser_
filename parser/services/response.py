import logging
from parser.models import ParseTask, SiteParseSettings
from parser.services.types import ParseResult
from parser.services.utils import extract_number

from jsonpath_ng import parse
from lxml import html

log = logging.getLogger(__name__)


def process_css(settings: SiteParseSettings, res: str, task: ParseTask, multiple: bool = False) -> list[ParseResult]:
    """Process css using lxml"""
    tree = html.fromstring(res)

    path_title = settings.path_title
    path_price = settings.path_price

    res_title = tree.cssselect(path_title)
    res_price = tree.cssselect(path_price)

    res: list[ParseResult] = []
    log.debug(f"CSS Process result: {res_title} | {res_price}")

    if len(res_title) != len(res_price):
        task.log.warning(f"Parsed titles ({len(res_title)}) count differs from price {len(res_price)}.")

    for title, price in zip(res_title, res_price):
        task.log.debug(f"Raw price text(css): {price.text}")
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

    if len(res_title) != len(res_price):
        task.log.warning(f"Parsed titles ({len(res_title)}) count differs from price {len(res_price)}.")

    for title, price in zip(res_title, res_price):
        task.log.debug(f"Raw price text(json): {price.value}")
        try:
            res.append(ParseResult(title=title.value, price=extract_number(price.value)))
        except Exception as e:
            task.log.error("JSON row processing error", exc_info=e)

    return res


def parse_result(settings: SiteParseSettings, res: str | dict, task: ParseTask, multiple: bool = False):
    """Parse request result"""

    if isinstance(res, dict):
        result = process_json(settings, res, task, multiple=multiple)
    else:
        result = process_css(settings, res, task, multiple=multiple)

    for item in result:
        if item.title:
            item.title = item.title.strip()

    return result
