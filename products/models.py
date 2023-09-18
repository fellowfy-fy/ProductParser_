from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class WithDates(models.Model):
    created_at = models.DateTimeField("Дата создания", auto_now_add=True, null=True)
    updated_at = models.DateTimeField("Дата редактирования", auto_now=True, null=True)

    class Meta:
        abstract = True


class Product(WithDates, models.Model):
    name = models.CharField("Название товара", max_length=255)
    synonyms = models.TextField("Синонимы товара", blank=True)

    categories = models.ManyToManyField("Category", blank=True, related_name="products")
    linked_id = models.CharField("Связь", max_length=255, blank=True, null=True)
    price = models.FloatField("Цена")
    task = models.ForeignKey(
        "parser.ParseTask",
        models.SET_NULL,
        related_name="task_created",
        null=True,
        blank=True,
        verbose_name="Создано задачей",
    )
    author = models.ForeignKey(
        User, models.CASCADE, related_name="products", verbose_name="Автор задачи", null=True, blank=True
    )
    history: models.QuerySet["ProductPriceHistory"]

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class ProductPriceHistory(WithDates, models.Model):
    product = models.ForeignKey(Product, models.CASCADE, related_name="history")
    price = models.FloatField("Цена")
    task = models.ForeignKey(
        "parser.ParseTask",
        models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Создано задачей",
    )
    parse_settings = models.ForeignKey(
        "parser.SiteParseSettings",
        models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Использованы настройки парсинга",
    )

    class Meta:
        verbose_name = "История цен"
        verbose_name_plural = "История цен"


class Category(WithDates, models.Model):
    name = models.CharField("Название раздела", max_length=255, unique=True)
    author = models.ForeignKey(
        User, models.CASCADE, related_name="categories", verbose_name="Автор задачи", null=True, blank=True
    )
    products: models.QuerySet["Product"]

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"

    def __str__(self):
        return self.name
