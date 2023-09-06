from parser.models import SiteParseSettings
from urllib.parse import urlparse

from django.template import Context, Template

from products.models import Product


def extract_domain(url: str) -> str:
    """Extract domain from URL"""
    return urlparse(url).netloc


def process_variables(settings: SiteParseSettings, text: str, product: Product | None = None) -> str:
    """Process variables in template"""
    t = Template(text)
    c = Context(
        {
            "product": product,
            "settings": settings,
        }
    )
    return t.render(c)
