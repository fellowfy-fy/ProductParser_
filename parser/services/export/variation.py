from datetime import date
from parser.services.export.base import CellValue
from parser.services.export.current_prices import CellInfo, ExcelExportCurrentPrices

from products.models import Product


class ExcelExportVariation(ExcelExportCurrentPrices):
    name = "prices_variation"

    def process_headers(self, settings, product: Product):
        headers = [
            product.name,
            "Наша компания",
        ]
        for settings_item in settings:
            headers.append(f"Конкурент {settings_item.domain}")
            headers.append("Отклонение")
        ##
        self.insert_headers(headers)

    def process_product_setting(self, product, setting) -> list[CellInfo]:
        last_price = self.get_product_last_history_price(product, setting)
        url, price = [CellInfo(setting.url), CellInfo(None)]
        if last_price:
            price.value = last_price

        return [url, price]

    def sheet_process(self) -> None:
        products, settings = self._get_products()
        if products:
            self.delete_initial_sheet()

        for product in products:
            self.create_sheet(f"Продукт #{product.pk}")
            self.process_headers(settings, product)
            values: list[CellValue] = [
                product.name,
                product.price,
                0,
            ]
            ##
            last_settings_values = {}

            for dt in self.get_dates_list():
                values = [
                    dt.strftime("%d.%b"),
                    product.price,
                ]

                for setting in settings:
                    price = self.get_date_price(product, setting, dt)
                    variation = 0
                    if price.value and setting.pk in last_settings_values:
                        variation = last_settings_values[setting.pk] - price.value
                    if price.value:
                        last_settings_values[setting.pk] = price.value

                    values.append(price)
                    values.append(variation)

                self.insert_row(values)

    def get_date_price(self, product: Product, settings, date: date) -> CellInfo:
        price = CellInfo()

        date_values = {}
        for item in product.history.all():
            item_date = item.created_at.replace(tzinfo=None)

            if not item.parse_settings or not item.parse_settings.pk == settings.pk:
                continue
            if item_date.date() > date:
                continue
            date_values[item_date] = item.price

            # print(item, item.price)
        if date_values:
            max_date = max(date_values)
            if max_date:  # Last date found
                # print(date, date_values)
                price.value = date_values[max_date]

        return price
