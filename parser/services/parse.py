import logging
from dataclasses import dataclass
from parser.models import ParseTask, SiteParseSettings, TaskStatusChoices
from parser.services.request import send_request
from parser.services.response import ParseResult, parse_result
from parser.services.utils import detect_url_settings, extract_urls, process_variables
from typing import Callable

from products.models import Product, ProductPriceHistory

log = logging.getLogger(__name__)


@dataclass
class ProcessResult:
    parse_result: list[ParseResult]
    settings: SiteParseSettings
    task: ParseTask
    product: Product | None = None


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


def process_parse_results(res: list[ProcessResult | None]):
    for item_res in res:
        if item_res:
            process_parse_result(item_res)


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


def process_task(task: ParseTask, callback: Callable | None = None):
    """Process parse task"""
    urls = extract_urls(task.urls)
    res: list[ProcessResult | None] = []

    task.status = TaskStatusChoices.RUN
    task.save(update_fields=["status"])

    if task.products:  # Products detect mode
        url = urls[0]
        assert url is not None, "URL list empty"
        log.debug("Processing products list...")

        all_products = task.products.all()
        for i, product in enumerate(all_products):
            res.append(process_task_url(task, url, product=product))
            if callback:
                callback(i, len(all_products))

    else:
        for i, url in enumerate(urls):
            res.append(process_task_url(task, url))
            if callback:
                callback(i, len(urls))

    process_parse_results(res)
    task.status = TaskStatusChoices.PAUSED
    task.save(update_fields=["status"])

    return res
