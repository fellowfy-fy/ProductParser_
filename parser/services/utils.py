import re
from parser.models import ParseTask, SiteParseSettings
from urllib.parse import urlparse

from django.db.models import Q
from django.template import Context, Template
from fuzzywuzzy import fuzz

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


def url_regex(match_regex: str, url_task: str, url_settings: str) -> str:
    """Replace url_settings with extracted regex values from url_task"""
    match = re.search(match_regex, url_task)
    if match:
        replaces: dict[str, str] = {}

        for idx, group in enumerate(match.groups(), 1):
            replaces[str(idx)] = group

        # res = url_settings.format(**replaces)
        res = url_settings.format(*replaces.values())
        return res

    return url_settings


def select_best_settings(url: str, settings: list[SiteParseSettings]):
    best_setting: SiteParseSettings | None = None
    best_score: int = 0

    for setting in settings:
        setting_url = setting.url_match or setting.url
        score = fuzz.ratio(url, setting_url)
        if score > best_score:
            best_score = score
            best_setting = setting

    return (best_setting, best_score)


def detect_url_settings(url: str, task: ParseTask | None = None) -> SiteParseSettings | None:
    """Detect SiteParseSettings by url"""
    matching_settings = SiteParseSettings.objects.filter(
        Q(domain=extract_domain(url))
        | Q(url_match__startswith="https://" + extract_domain(url))
        | Q(url_match__startswith=url)
    ).all()
    if task:
        task.log.warning(f"Found multiple parser settings: {matching_settings}")
        best_settings, best_score = select_best_settings(url, matching_settings)
        if best_settings:
            return best_settings

    return matching_settings[0] if matching_settings else None


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

    text = text.lower().replace("&nbsp;", "")
    text = re.sub(r"[а-я]+\d", "", text)
    text = re.sub(r"[^0-9,.]", "", text)  # м2 and others remove
    numbers = re.findall(r"[0-9,.]+", text)
    assert numbers is not None, "Numbers not found"
    cleared_str: str = numbers[0].replace(",", ".")
    # if re_match := re.search("[0-9]", cleared_str):
    #     start_index = re_match.start()
    #     end_index = len(cleared_str) - re.search("[0-9]", cleared_str[::-1]).start()
    #     cleared_str = cleared_str[start_index:end_index].strip()

    return float(cleared_str)


def translate_months(text: str) -> str:
    months = {
        "Jan": "Янв",
        "Feb": "Февр",
        "Mar": "Март",
        "Apr": "Апр",
        "May": "Май",
        "Jun": "Июнь",
        "Jul": "Июль",
        "Aug": "Авг",
        "Sep": "Сент",
        "Oct": "Окт",
        "Nov": "Нояб",
        "Dec": "Дек",
    }
    for k, v in months.items():
        text = text.replace(k, v)

    return text
