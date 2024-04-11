from parser.services.export.base import CellValue
from parser.models import SiteParseSettings
from products.models import Product
from parser.services.export.current_prices import ExcelExportCurrentPrices

class ExcelExportCompetitors(ExcelExportCurrentPrices):
    name = "prices_competitors"


    def get_product_date_history_competitor(self, product: Product, setting: SiteParseSettings):
        histories = product.history.filter(parse_settings=setting).order_by("-created_at")
        prices = [history.price for history in histories]
        competitors = [history.competitor for history in histories]
        return prices, competitors


    def process_headers(self, settings):
        headers = [
            "Товар",
            "Сайт",
            "Цена",
            "Статус",
            "Категория",
            "Конкурент",
        ]
        ##
        self.insert_headers(headers)

    def sheet_process(self) -> None:
        products, settings = self._get_products()
        self.process_headers(settings)

        for product in products:
            for setting in settings:
                prices, competitors = self.get_product_date_history_competitor(product, setting)\
                
                for price, competitor in zip(prices, competitors):
                    status_names = [cat.name for cat in product.statusproducts.all()] if product.statusproducts.exists() else ["Без категории"]
                    status = ", ".join(status_names)
                    category_names = [cat.name for cat in product.categories.all()] if product.categories.exists() else ["Без категории"]
                    category = ", ".join(category_names)
                    values: list[CellValue] = [
                        product.name,
                        f"{setting.domain}",
                        price or 0,
                        status,
                        category,
                        competitor or "Unknown",
                    ]
                    self.insert_row(values)
