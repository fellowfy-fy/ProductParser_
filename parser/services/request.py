import logging
from parser.models import SiteParseSettings
from parser.services.utils import process_variables

import httpx

log = logging.getLogger(__name__)


def send_request(settings: SiteParseSettings, url: str | None = None) -> str | dict:
    full_url = process_variables(settings, url or settings.url)
    log.debug(
        f"""Request info:
data={settings.request_data},
headers={settings.request_headers},
method={settings.request_method},
url={full_url}"""
    )
    resp = httpx.request(
        settings.request_method,
        url=full_url,
    )
    # data=settings.request_data or {},
    # headers=settings.request_headers or {},

    if settings.parse_mode == SiteParseSettings.ParseMode.JSON:
        return resp.json()

    return resp.text
