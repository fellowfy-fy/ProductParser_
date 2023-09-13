from parser.models import ParseTask, SiteParseSettings

from attr import dataclass

from products.models import Product


@dataclass
class ParseResult:
    title: str
    price: float


@dataclass
class ProcessResult:
    parse_result: list[ParseResult]
    settings: SiteParseSettings
    task: ParseTask
    product: Product | None = None
