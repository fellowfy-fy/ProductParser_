from parser.services.export.base import CellColor
from parser.services.export.current_prices import CellInfo, ExcelExportCurrentPrices


class ExcelExportPriceDynamics(ExcelExportCurrentPrices):
    name = "prices_dynamics"

    def process_product_setting(self, product, setting) -> list[CellInfo]:
        last_price = self.get_product_last_history_price(product, setting)
        current_price = self.get_product_date_history_price(product, setting)
        url, price = [CellInfo(setting.url), CellInfo(None)]
        if last_price:
            price.value = last_price

        if last_price and current_price:
            if current_price > last_price:
                price.color = CellColor.RED
            elif current_price < last_price:
                price.color = CellColor.GREEN

        return [url, price]
