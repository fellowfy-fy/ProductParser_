from parser.models import SiteParseSettings
from parser.services.request.base import BaseRequestHandler

import httpx


class HttpxRequesthandler(BaseRequestHandler):
    def send_request(self, settings: SiteParseSettings, url: str | None = None):
        """Process single request"""
        full_url = self._get_url(settings, url)
        data = self._get_request_data(settings)
        headers = self._get_request_headers(settings)
        self.log.debug(
            f"""Request info:
method={settings.request_method},
url={full_url}
data={data},
headers={headers},
"""
        )
        resp = httpx.request(
            settings.request_method,
            url=full_url,
            data=data,
            headers=headers,
        )

        if settings.parse_mode == SiteParseSettings.ParseMode.JSON:
            return resp.json()

        return resp.text
