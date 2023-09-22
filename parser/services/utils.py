import re
from parser.models import SiteParseSettings
from urllib.parse import urlparse

from django.db.models import Q
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


def detect_url_settings(url: str) -> SiteParseSettings | None:
    """Detect SiteParseSettings by url"""
    matching_settings = SiteParseSettings.objects.filter(
        Q(domain=extract_domain(url))
        | Q(url_match__startswith="https://" + extract_domain(url))
        | Q(url_match__startswith=url)
    ).all()

    return matching_settings[0] if matching_settings else None  # TODO: better settings detect algorithm


def extract_urls(text: str) -> list[str]:
    """Split text into urls"""
    return list(filter(None, text.split("\n")))


def validate_urls(text: str):
    """Return all not valid URL"""
    urls = extract_urls(text)
    undetected = []

    for url in urls:
        detected = detect_url_settings(url)
        if not detected:
            undetected.append(url)

    return undetected


def extract_number(text: str | int) -> float:
    """Clear string from non-digits. Clears all non digits outside, keeps dot inside."""
    if isinstance(text, int):
        return text

    text = text.replace("&nbsp;", "")
    text = re.sub("[^ 0-9,.]", "", text)
    numbers = re.findall("[0-9,.]+", text)
    assert numbers is not None, "Numbers not found"
    cleared_str: str = numbers[0].replace(",", ".")
    # if re_match := re.search("[0-9]", cleared_str):
    #     start_index = re_match.start()
    #     end_index = len(cleared_str) - re.search("[0-9]", cleared_str[::-1]).start()
    #     cleared_str = cleared_str[start_index:end_index].strip()

    return float(cleared_str)
