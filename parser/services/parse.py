from dataclasses import dataclass
import logging
from parser.models import ParseTask, SiteParseSettings
from parser.services.request import send_request
from parser.services.response import ParseResult, parse_result
from parser.services.utils import extract_domain, process_variables
from django.db.models import Q

from products.models import Product, ProductPriceHistory

log = logging.getLogger(__name__)


@dataclass
class ProcessResult:
    parse_result: list[ParseResult]
    settings: SiteParseSettings
    task: ParseTask
    product: Product | None = None


def detect_url_settings(url: str) -> SiteParseSettings | None:
    """Detect SiteParseSettings by url"""
    matching_settings = SiteParseSettings.objects.filter(
        Q(domain=extract_domain(url)) | Q(url_match__startswith=extract_domain(url)) | Q(url_match__startswith=url)
    ).all()

    return matching_settings[0] if matching_settings else None  # TODO: better settings detect algorithm


def process_parse_result(res: ProcessResult):
    """Process single parsing result"""
    if res.product:  # Update product
        assert len(res.parse_result) > 0, "No results"
        single_result = res.parse_result[0]
        ProductPriceHistory.objects.create(
            product=res.product,
            price=single_result.price,
            task=res.task,
        )


def process_parse_results(res: list[ProcessResult]):
    for i in res:
        process_parse_result(i)


def process_task_url(task: ParseTask, url: str, product: Product | None = None) -> ProcessResult | None:
    """Process single task url"""
    settings = detect_url_settings(url)
    if not settings:
        log.warning(f"Settings not found for url: '{url}' ({task})")
        return None
    ##
    request_url = settings.url if settings.force_parser_url else url or settings.url

    response = send_request(settings, url=process_variables(settings, request_url, product=product))

    log.debug(f"Raw response: {response}")
    result = parse_result(settings, response)
    log.debug(f"Raw Result: {result}")

    return ProcessResult(
        parse_result=result,
        settings=settings,
        product=product,
        task=task,
    )


def process_task(task: ParseTask):
    """Process parse task"""
    urls = list(filter(None, task.urls.split(" ")))
    res: list[ProcessResult] = []

    if task.products:  # Products detect mode
        url = urls[0]
        assert url is not None, "URL list empty"
        log.debug("Processing products list...")

        for product in task.products.all():
            res.append(process_task_url(task, url, product=product))

    else:
        for url in urls:
            res.append(process_task_url(task, url))

    process_parse_results(res)

    return res
