from parser.models import SiteParseSettings

import httpx

from parser.services.utils import process_variables


def send_request(settings: SiteParseSettings, url: str | None = None) -> str | dict:
    resp = httpx.request(
        settings.request_method,
        url=process_variables(settings, url or settings.url),
        data=settings.request_data,
        headers=settings.request_headers,
    )

    if settings.parse_mode == SiteParseSettings.ParseMode.JSON:
        return resp.json()

    return resp.text
