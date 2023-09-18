import statistics
from parser.models import SiteParseSettings
from parser.services.export.base import BaseExcelExport

from django.db.models import Q, QuerySet

from accounts.models import RoleChoices
from accounts.utils import get_user_role
from products.models import Product


class ExcelExportCurrentPrices(BaseExcelExport):
    name = "current_prices"

    def _get_settings_by_ids(self, settings_ids: list[int]):
        """Get parse settings by ids"""
        all_settings_ids = list(filter(None, settings_ids))  # Filter from None
        all_settings = SiteParseSettings.objects.filter(id__in=all_settings_ids).all()
        return all_settings

    def _get_available_products(self):
        user = self.params.user
        role = get_user_role(user)

        if filter_task := self.params.filter_task:
            return Product.objects.filter(task=filter_task)

        if role == RoleChoices.ADMIN:
            return Product.objects.all()
        elif role == RoleChoices.MANAGER:
            return Product.objects.filter(Q(author=user) | Q(author__manager=user))
        return Product.objects.filter(author=user)

    def _get_products(self):
        if self.params.filter_product:
            products = [self.params.filter_product]
            self.log.info(f"Filtering by product: {products}")
            all_settings_ids = self.params.filter_product.history.values_list("parse_settings", flat=True).distinct()
        else:
            self.log.info("Retrieving all products...")
            products = self._get_available_products().prefetch_related("history")
            all_settings_ids = products.values_list("history__parse_settings", flat=True).distinct()

        settings = self._get_settings_by_ids(all_settings_ids)
        self.log.info(f"Found products: {len(products)}")
        self.log.info(f"Found all settings ({len(settings)}): {settings}")
        return products, settings

    def apply_filter_date1_created_lt(self, qs: QuerySet):
        if not self.params.date_from:
            return qs
        return qs.filter(date_created__lt=self.params.date_from)

    def sheet_process(self):
        headers = [
            "Наименование товара [товар из справочника, указанный в Задании]",
            "Цена этого товара [товар из справочника, указанный в Задании]",
            "Средняя цена по итогу анализа [среднее значение цен конкурентов]",
        ]

        products, settings = self._get_products()

        for settings_item in settings:
            headers.append(f"Ссылка на карту товара конкурента {settings_item.domain}")
            headers.append(f"Цена товара {settings_item.domain}")
        ##
        self.insert_headers(headers)
        ##

        for product in products:
            values = [
                product.name,
                product.price,
                0,
            ]
            ##
            prices: list[int] = []
            for setting in settings:
                last_history = (
                    self.apply_filter_date1_created_lt(product.history.filter(parse_settings=setting))
                    .order_by("-created_at")
                    .first()
                )
                # self.log.debug(f"Last history: {last_history}")
                if last_history:
                    values.append(setting.url)
                    values.append(last_history.price)
                    prices.append(last_history.price)
                else:
                    values.extend([None, None])

            ##
            values[2] = statistics.mean(prices)
            self.insert_row(values)
