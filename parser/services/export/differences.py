import locale
import statistics
from datetime import date, datetime, timedelta
from parser.services.export.base import CellColor, CellValue
from parser.services.export.current_prices import CellInfo, ExcelExportCurrentPrices

from products.models import Product


class ExcelExportDifferences(ExcelExportCurrentPrices):
    name = "prices_differences"

    base_headers: list[str] = []

    def _get_dates(self):
        """Get params dates or default"""
        start_date = self.params.date_from
        end_date = self.params.date_to
        if not end_date:
            end_date = datetime.today()
        if not start_date:
            start_date = datetime.today() - timedelta(days=15)

        return start_date, end_date

    def get_dates_list(self):
        start_date, end_date = self._get_dates()

        delta = end_date - start_date
        r = []

        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            r.append(day.date())

        return r

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
        start_date, end_date = self._get_dates()

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

    # def process_product_setting(self, product, setting) -> list[CellInfo]:
    #     last_price = self.get_product_last_history_price(product, setting)
    #     current_price = self.get_product_date_history_price(product, setting)
    #     url, price = [CellInfo(setting.url), CellInfo(None)]
    #     if last_price:
    #         price.value = last_price

    #     print("Price change: ", last_price, current_price)
    #     if last_price and current_price:
    #         if current_price > last_price:
    #             price.color = CellColor.RED
    #         elif current_price < last_price:
    #             price.color = CellColor.GREEN

    #     return [url, price]
