import logging
from datetime import datetime
from parser.models import (
    MonitoringModeChoices,
    ParseTask,
    TaskStatusChoices,
)
from parser.services.request.base import BaseRequestHandler
from parser.services.request.httpx import HttpxRequesthandler
from parser.services.request.selenium import SeleniumRequesthandler
from parser.services.response import parse_result
from parser.services.types import ProcessResult
from parser.services.utils import detect_url_settings, extract_urls, process_variables, url_regex
from typing import Callable, Type

from products.models import Product, ProductPriceHistory

log = logging.getLogger(__name__)


class CacheRequestHandlers:
    cache: dict[str, BaseRequestHandler] = dict()
    task: ParseTask
    log: logging.Logger

    def __init__(self, task: ParseTask) -> None:
        self.cache = dict()
        self.task = task
        self.log = logging.getLogger("CacheHandler")

    def get_cache(self, key: str, cls_name: Type[BaseRequestHandler]):
        if res := self.cache.get(key):
            self.log.debug(f"Get from cache: {cls_name.__name__}")
            return res

        self.log.debug(f"Set cache: {cls_name.__name__}")
        res = cls_name(self.task)
        self.cache[key] = res
        return res

    def get_httpx_handler(self):
        return self.get_cache("httpx", HttpxRequesthandler)

    def get_selenium_handler(self):
        return self.get_cache("selenium", SeleniumRequesthandler)

    def teardown(self):
        for name, instance in self.cache.items():
            self.log.debug(f"Cache teardown: {instance.__class__.__name__}")
            instance.teardown()
        self.cache.clear()


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


def process_task_url(
    task: ParseTask, url: str, handler_cache: CacheRequestHandlers, product: Product | None = None
) -> ProcessResult | None:
    """Process single task url"""
    settings = detect_url_settings(url, task=task)
    if not settings:
        task.log.warning(f"Settings not found for url: '{url}' ({task})")
        return None
    task.log.debug(f"Selected settings: {settings}")
    ##
    request_url = settings.url if settings.force_parser_url else url or settings.url
    full_url = process_variables(settings, request_url, product=product)
    if settings.match_regex:
        task.log.debug(f"Using match regex for url: '{full_url}' ...")
        full_url = url_regex(settings.match_regex, url_task=full_url, url_settings=settings.url)

    task.log.debug(f"Sending task request {full_url}...")

    if settings.use_selenium:
        handler = handler_cache.get_selenium_handler()
    else:
        handler = handler_cache.get_httpx_handler()

    response = handler.send_request(settings, full_url)

    task.log.debug(f"Raw response: {response}")
    result = parse_result(settings=settings, res=response, task=task)
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

    handler_cache = CacheRequestHandlers(task)

    # -- Process task
    try:
        if task.products.count() > 0 and task.monitoring_mode != MonitoringModeChoices.CATALOG:  # Products detect mode

            all_products = task.products.all()
            for url in urls:
                task.log.info(f"Processing products list: {len(all_products)} ({url})...")
                for i, product in enumerate(all_products):
                    res.append(process_task_url(task=task, url=url, product=product, handler_cache=handler_cache))
                    if callback:
                        callback(i, len(all_products))

        else:
            task.log.info(f"Processing URLS list ({len(urls)})...")
            for i, url in enumerate(urls):
                res.append(process_task_url(task=task, url=url, handler_cache=handler_cache))
                if callback:
                    callback(i, len(urls))
    except Exception as exc:
        task.log.error("Task processing error", exc_info=exc)
    finally:
        handler_cache.teardown()

    # -- Task finished

    if not test:
        process_parse_results(task, res)
    else:
        task.log.debug("Test flag set, products not saved.")

    errors_count = task.log.level_count("error") + task.log.level_count("critical")
    if errors_count > 0:
        task.status = TaskStatusChoices.ERROR
        task.save(update_fields=["status"])
    elif task.status == TaskStatusChoices.RUN:
        task.status = TaskStatusChoices.PAUSED
        task.save(update_fields=["status"])

    return res
