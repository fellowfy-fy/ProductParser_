from parser.services.export.base import CellValue
from parser.services.export.current_prices import ExcelExportCurrentPrices


class ExcelExportCompetitors(ExcelExportCurrentPrices):
    name = "prices_competitors"

    def process_headers(self, settings):
        headers = [
            "Товар",
            "Конкурент",
            "Цена",
        ]
        ##
        self.insert_headers(headers)

    def sheet_process(self) -> None:
        products, settings = self._get_products()
        self.process_headers(settings)

        for product in products:
            for setting in settings:
                price = self.get_product_date_history_price(product, setting)

                values: list[CellValue] = [
                    product.name,
                    f"Конкурент: {setting.domain}",
                    price or 0,
                ]
                self.insert_row(values)
