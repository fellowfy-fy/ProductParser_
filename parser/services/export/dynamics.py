import statistics
from parser.services.export.current_prices import ExcelExportCurrentPrices


class ExcelExportPriceDynamics(ExcelExportCurrentPrices):
    name = "prices_dynamics"

    def sheet_process(self) -> None:
        products, settings = self._get_products()
        self.process_headers(settings)

        for product in products:
            values = [
                product.name,
                product.price,
                0,
            ]
            ##
            prices: list[int] = []
            colors: list[str | None] = [None, None, None]
            for setting in settings:
                last_price = self.get_product_last_history_price(product, setting)
                current_price = self.get_product_date_history_price(product, setting)
                colors_curr = []

                if last_price:
                    values.append(setting.url)
                    values.append(last_price)
                    prices.append(last_price)
                    color = None
                    if current_price > last_price:
                        color = self.color_red
                    elif current_price < last_price:
                        color = self.color_green
                    colors_curr.extend([None, color])
                else:
                    values.extend([setting.url, None])

                colors.extend(colors_curr)

            ##
            values[2] = statistics.mean(prices) if prices else 0
            self.insert_row(values)
            self.last_row_colors(colors)
