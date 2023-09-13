import logging
from parser.models import ParseTask, SiteParseSettings
from parser.services.utils import process_variables


class BaseRequestHandler:
    """Base HTTP request handler"""

    task: ParseTask
    log: logging.Logger

    def __init__(self, task: ParseTask):
        self.task = task
        self.log = logging.getLogger(__name__)
        self._init()

    def _init(self):
        """Handler init method. Called once on __init__."""
        pass

    def _get_url(self, settings: SiteParseSettings, url: str | None = None):
        """Get request url"""
        return process_variables(settings, url or settings.url)

    def _get_request_data(self, settings: SiteParseSettings):
        """Get request data"""
        if settings.request_data and isinstance(settings.request_data, dict):
            return settings.request_data
        return {}

    def _get_request_headers(self, settings: SiteParseSettings):
        """Get request headers"""
        if settings.request_headers and isinstance(settings.request_headers, dict):
            return settings.request_headers
        return {}

    def send_request(self, settings: SiteParseSettings, url: str | None = None) -> str | dict:
        raise NotImplementedError()

    def teardown(self):
        """Called when all requests are finishedт"""
        pass
