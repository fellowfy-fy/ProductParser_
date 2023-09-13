import os
import time
from parser.models import ParseTask, SiteParseSettings
from parser.services.request.base import BaseRequestHandler
from typing import Any

from selenium import webdriver
from selenium_driver_updater import DriverUpdater

SELENIUM_HEADLESS = not (os.getenv("SELENIUM_HEAD"))
SELENIUM_REMOTE = os.getenv("SELENIUM_REMOTE")
SELENIUM_VERSION = os.getenv("SELENIUM_VERSION")


class SeleniumRequesthandler(BaseRequestHandler):
    driver: webdriver.Chrome
    check_interval: int = 5  # Is page loaded checks count
    check_wait: int = 5  # Wait before starting checks
    load_timeout: int = 30  # Page load timeout
    headless: bool = SELENIUM_HEADLESS

    def __init__(self, task: ParseTask, headless: bool | None = None):
        super().__init__(task)
        if headless is not None:
            self.headless = headless

    def _init(self):
        self._driver_init()

    def _driver_init(self):
        # base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "drivers")
        self.log.info("Init selenium driver...")

        if SELENIUM_REMOTE:
            options = self._get_driver_options(remote=True)

        updater_kwargs = self._get_updated_kwargs()

        base_dir = "drivers"
        filename = DriverUpdater.install(path=base_dir, driver_name=DriverUpdater.chromedriver, **updater_kwargs)
        options = self._get_driver_options(remote=False)

        self.driver = webdriver.Chrome(service=webdriver.ChromeService(executable_path=filename), options=options)

    def _get_driver_options(self, remote: bool = False):
        options = webdriver.ChromeOptions()
        if remote:
            options.debugger_address = SELENIUM_REMOTE
        else:
            if self.headless:
                options.add_argument("--headless=new")
                options.add_argument("--disable-gpu")

        return options

    def _get_updated_kwargs(self) -> dict:
        """DriverUpdater kwargs"""
        res: dict[str, Any] = {}
        if SELENIUM_VERSION:
            res["version"] = SELENIUM_VERSION
            res["check_driver_is_up_to_date"] = False
        else:
            res["check_driver_is_up_to_date"] = True
            res["upgrade"] = True

        res["check_browser_is_up_to_date"] = False
        return res

    def page_has_loaded(self):
        self.log.info("Checking if {} page is loaded.".format(self.driver.current_url))
        page_state = self.driver.execute_script("return document.readyState;")
        return page_state == "complete"

    def send_request(self, settings: SiteParseSettings, url: str | None = None):
        """Process single request"""
        full_url = self._get_url(settings, url)

        self.driver.get(full_url)
        time.sleep(self.check_wait)

        for i in range(int(self.load_timeout / self.check_interval)):
            if self.page_has_loaded():
                break
            time.sleep(self.check_interval)

        return self.driver.page_source

    def teardown(self):
        self.log.info("Selenium teardown")
        self.driver.quit()
