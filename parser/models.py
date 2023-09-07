import logging
from urllib.parse import urlparse

from computedfields.models import ComputedFieldsModel, computed
from django.contrib.auth import get_user_model
from django.db import models
from multiselectfield.db.fields import MultiSelectField

from products.models import Product

User = get_user_model()


class TaskStatusChoices(models.IntegerChoices):
    CREATED = 1, "Создана"
    RUN = 2, "В работе"
    CANCELLED = 3, "Отменена"
    PAUSED = 4, "Пауза"
    STOPPED = 5, "Остановлена"


class TaskPeriodChoices(models.IntegerChoices):
    DAILY = 1, "Ежедневно"
    TWO_MONTHLY = 2, "Дважды в месяц"
    MONTHLY = 3, "Раз в месяц"
    QUARTER = 4, "Ежеквартально"
    ONETIME = 5, "Единоразово"


class MonitoringTypeChoices(models.TextChoices):
    REPORTS = "report", "Отчеты"
    EXPORT = "export", "Выгрузка"


class MonitoringModeChoices(models.IntegerChoices):
    STRICT = 1, "Строгий мониторинг"
    FLEXIBLE = 2, "Гибкий мониторинг"
    CATALOG = 3, "Получение каталогов"


class WorkModeChoices(models.IntegerChoices):
    NOTHING = 1, "Текущие цены"
    DYNAMICS = 2, "Динамика"
    DIFFERENCES = 3, "Отличия"


class NotificationTargetChoices(models.TextChoices):
    PRICE_DECREASED = "decr", "Цена конкурента уменьшилась"
    PRICE_INCREASED = "incr", "Цена конкурента увеличилась"


class ParseTask(models.Model):
    name = models.CharField("Название задачи", max_length=100, null=True, blank=False)
    status = models.IntegerField("Статус", choices=TaskStatusChoices.choices, default=TaskStatusChoices.CREATED)
    author = models.ForeignKey(User, models.CASCADE, related_name="tasks", verbose_name="Автор задачи")

    period = models.PositiveSmallIntegerField(
        "Периодичность мониторинга",
        choices=TaskPeriodChoices.choices,
        default=TaskPeriodChoices.DAILY,
    )
    period_date1 = models.DateField("Дата 1", null=True, blank=True)
    period_date2 = models.DateField("Дата 2", null=True, blank=True)

    monitoring_mode = models.PositiveSmallIntegerField(
        "Режим мониторинга", choices=MonitoringModeChoices.choices, default=MonitoringModeChoices.STRICT
    )
    monitoring_type = MultiSelectField("Тип мониторинга", choices=MonitoringTypeChoices.choices, max_length=20)
    work_mode = models.IntegerField("Режим работы", choices=WorkModeChoices.choices)
    products = models.ManyToManyField(Product, related_name="tasks", blank=True)
    urls = models.TextField("URL сайтов", null=True, blank=False)

    notifications_enable = models.BooleanField("Отправлять уведомления", default=False)
    notifications_target = MultiSelectField(
        "Цель уведомления",
        choices=NotificationTargetChoices.choices,
        null=True,
        blank=True,
        max_length=20,
    )

    created_at = models.DateTimeField("Дата создания", auto_now_add=True, null=True)
    updated_at = models.DateTimeField("Дата редактирования", auto_now=True, null=True)

    class Meta:
        verbose_name = "Задача парсера"
        verbose_name_plural = "Задачи парсера"

    def __str__(self):
        return self.name


class SiteParseSettings(ComputedFieldsModel, models.Model):
    class ParseMode(models.IntegerChoices):
        HTML = 1, "HTML"
        JSON = 2, "JSON"

    class HTTPMethod(models.TextChoices):
        GET = "GET", "GET"
        POST = "POST", "POST"

    url = models.URLField("Адрес страницы запроса", max_length=500)
    url_match = models.URLField("Адрес страницы задачи", max_length=500, null=True, blank=True)

    parse_mode = models.PositiveSmallIntegerField("Режим парсинга", choices=ParseMode.choices, default=ParseMode.HTML)
    request_method = models.CharField("HTTP метод", max_length=5, choices=HTTPMethod.choices, default=HTTPMethod.GET)
    request_headers = models.JSONField(
        "Заголовки запроса",
        null=True,
        blank=True,
    )
    request_data = models.JSONField(
        "Данные запроса",
        null=True,
        blank=True,
    )

    path_title = models.TextField("Путь к названию товара")
    path_price = models.TextField("Путь к цене товара")

    # Path value can be either jsonpath or css expression depending on parse mode
    # Path supports variables
    force_parser_url = models.BooleanField("Принудительно использовать URL парсера", default=False)

    @computed(models.CharField(max_length=100, null=True), depends=[("self", ["url"])])
    def domain(self):
        try:
            return urlparse(self.url).netloc
        except Exception as e:
            logging.warning("URL parse exception", exc_info=e)
            return ""

    class Meta:
        verbose_name = "Настройки парсинга сайта"
        verbose_name_plural = "Настройки парсинга сайта"

    def __str__(self):
        return self.domain or self.url
