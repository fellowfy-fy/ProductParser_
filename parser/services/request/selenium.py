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
    remote_chrome_addr: str | None = None  # Remote address
    remote_grid_addr: str | None = None

    def __init__(self, task: ParseTask, headless: bool | None = None):
        super().__init__(task)
        if headless is not None:
            self.headless = headless

    def _init(self):
        if remote := SELENIUM_REMOTE:
            if remote.startswith("http"):
                self.remote_grid_addr = SELENIUM_REMOTE
            else:
                self.remote_chrome_addr = SELENIUM_REMOTE

        self._driver_init()

    def _driver_init(self):
        # base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "drivers")
        assert not (
            self.remote_grid_addr and self.remote_chrome_addr
        ), "Only one option of options remote_grid_addr / remote_chrome_addr should be used"
        self.log.info("Init selenium driver...")

        updater_kwargs = self._get_updated_kwargs()

        base_dir = "drivers"
        filename = DriverUpdater.install(path=base_dir, driver_name=DriverUpdater.chromedriver, **updater_kwargs)
        options = self._get_driver_options()

        if self.remote_grid_addr:
            self.log.info(f"Using remote selenium grid: {self.remote_grid_addr}")
            self.driver = webdriver.Remote(command_executor=self.remote_grid_addr, options=options)
        else:
            self.driver = webdriver.Chrome(service=webdriver.ChromeService(executable_path=filename), options=options)

        self._driver_post_init()

    def _driver_post_init(self):
        # -- Anti-bot pos init
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def _get_driver_options(self):
        options = webdriver.ChromeOptions()

        if self.remote_chrome_addr:
            self.log.info(f"Using remote selenium browser: {self.remote_chrome_addr}")
            options.debugger_address = self.remote_chrome_addr
        else:
            if self.headless:
                options.add_argument("--headless=new")
                options.add_argument("--disable-gpu")

        # -- Anti-bot
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

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
