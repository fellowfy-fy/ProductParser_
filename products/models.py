from django.db import models


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
        null=True,
        blank=True,
        verbose_name="Создано задачей",
    )

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


class Category(WithDates, models.Model):
    name = models.CharField("Название раздела", max_length=255, unique=True)

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"

    def __str__(self):
        return self.name
