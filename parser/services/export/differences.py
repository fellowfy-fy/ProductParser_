import locale
import statistics
from datetime import date
from parser.services.export.base import CellColor, CellValue
from parser.services.export.current_prices import CellInfo, ExcelExportCurrentPrices

from products.models import Product


class ExcelExportDifferences(ExcelExportCurrentPrices):
    name = "prices_differences"

    base_headers: list[str] = []

    def process_headers(self, product: Product):
        locale.setlocale(locale.LC_TIME, "ru_RU")
        headers = [
            product.name,
        ]

        for dt in self.get_dates_list():
            headers.append(dt.strftime("%d.%b"))

        ##
        self.insert_headers(headers)

    def sheet_process(self) -> None:
        products, settings = self._get_products()
        if products:
            self.delete_initial_sheet()

        for product_idx, product in enumerate(products):
            self.create_sheet(f"Продукт #{product.pk}")
            self.process_headers(product)

            settings_prices = {}

            for dt in self.get_dates_list():
                settings_prices[dt] = []

            for setting in settings:
                values: list[CellValue] = [
                    str(setting.domain),
                ]
                prices = []

                for dt in self.get_dates_list():
                    price = self.get_date_price(product, setting, dt)
                    if price.value:
                        settings_prices[dt].append(price.value)
                        prices.append(price.value)

                    values.append(price)
                self.insert_row(values)
            ##
            values_ours = [
                "Наша компания",
            ]
            for day in self.get_dates_list():
                day_prices = settings_prices[day]
                mean_price = 0
                color = None
                our_price = product.price
                if day_prices:
                    mean_price = statistics.mean(day_prices)

                if mean_price:
                    if mean_price > our_price:
                        color = CellColor.GREEN
                    elif mean_price < our_price:
                        color = CellColor.RED

                values_ours.append(
                    CellInfo(our_price, color=color),
                )

            self.insert_row(values_ours, 2)

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
