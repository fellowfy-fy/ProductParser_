import logging
from dataclasses import dataclass
from datetime import datetime
from parser.models import (
    MonitoringModeChoices,
    ParseTask,
    SiteParseSettings,
    TaskStatusChoices,
)
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


def process_parse_result(task: ParseTask, res: ProcessResult):
    """Process single parsing result"""
    if res.task.monitoring_mode == MonitoringModeChoices.CATALOG:
        task.log.info(f"Updating parsed products: {len(res.parse_result)} (settings #{res.settings.pk})")
        # Parse products
        for result in res.parse_result:
            product, _ = Product.objects.get_or_create(
                name__icontains=result.title,
                default={
                    "price": 0,
                    "task": res.task,
                    "author": res.task.author,
                },
            )
            ProductPriceHistory.objects.create(
                product=product, price=result.price, task=res.task, parse_settings=res.settings
            )
    else:  # Update existing product
        task.log.info(f"Updating existing products: {len(res.parse_result)} (settings #{res.settings.pk})")
        if res.product:
            assert len(res.parse_result) > 0, "No results"
            single_result = res.parse_result[0]
            ProductPriceHistory.objects.create(
                product=res.product, price=single_result.price, task=res.task, parse_settings=res.settings
            )


def process_parse_results(task: ParseTask, res: list[ProcessResult | None]):
    for item_res in res:
        if item_res:
            process_parse_result(task, item_res)


def process_task_url(task: ParseTask, url: str, product: Product | None = None) -> ProcessResult | None:
    """Process single task url"""
    settings = detect_url_settings(url)
    if not settings:
        task.log.warning(f"Settings not found for url: '{url}' ({task})")
        return None
    task.log.debug(f"Selected settings: {settings}")
    ##
    request_url = settings.url if settings.force_parser_url else url or settings.url
    full_url = process_variables(settings, request_url, product=product)

    task.log.debug(f"Sending task request {full_url}...")
    response = send_request(settings, url=full_url)

    task.log.debug(f"Raw response: {response}")
    result = parse_result(settings, response, task)
    if result:
        task.log.debug(f"Raw Result: {result}")
    else:
        task.log.error(f"Empty parsing result: {result}")
        task.status = TaskStatusChoices.ERROR
        task.save(update_fields=["status"])

    return ProcessResult(
        parse_result=result,
        settings=settings,
        product=product,
        task=task,
    )


def process_task(task: ParseTask, callback: Callable | None = None, test: bool = False):
    """Process parse task"""
    task.log.clear()

    urls = extract_urls(task.urls)
    res: list[ProcessResult | None] = []

    task.status = TaskStatusChoices.RUN
    task.last_run_at = datetime.now()
    task.save(update_fields=["status", "last_run_at"])

    if task.products.count() > 0 and task.monitoring_mode != MonitoringModeChoices.CATALOG:  # Products detect mode

        all_products = task.products.all()
        for url in urls:
            task.log.info(f"Processing products list: {len(all_products)} ({url})...")
            for i, product in enumerate(all_products):
                res.append(process_task_url(task, url, product=product))
                if callback:
                    callback(i, len(all_products))

    else:
        task.log.info(f"Processing URLS list ({len(urls)})...")
        for i, url in enumerate(urls):
            res.append(process_task_url(task, url))
            if callback:
                callback(i, len(urls))

    if not test:
        process_parse_results(task, res)
    else:
        task.log.debug("Test flag set, products not saved.")

    if task.status == TaskStatusChoices.RUN:
        task.status = TaskStatusChoices.PAUSED
        task.save(update_fields=["status"])

    return res
