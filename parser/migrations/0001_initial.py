# Generated by Django 4.2.2 on 2023-06-14 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0002_alter_product_options_productpricehistory"),
    ]

    operations = [
        migrations.CreateModel(
            name="ParseTask",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (1, "Создана"),
                            (2, "В работе"),
                            (3, "Отменена"),
                            (4, "Пауза"),
                            (5, "Остановлена"),
                        ],
                        verbose_name="Статус",
                    ),
                ),
                (
                    "monitoring_mode",
                    multiselectfield.db.fields.MultiSelectField(
                        choices=[("report", "Отчеты"), ("export", "Выгрузка")],
                        max_length=20,
                        verbose_name="Режим мониторинга",
                    ),
                ),
                (
                    "monitoring_type",
                    multiselectfield.db.fields.MultiSelectField(
                        choices=[("report", "Отчеты"), ("export", "Выгрузка")],
                        max_length=20,
                        verbose_name="Тип мониторинга",
                    ),
                ),
                (
                    "work_mode",
                    models.IntegerField(
                        choices=[(1, "Текущие цены"), (2, "Динамика"), (3, "Отличия")],
                        verbose_name="Режим работы",
                    ),
                ),
                (
                    "urls",
                    models.TextField(blank=True, null=True, verbose_name="URL сайтов"),
                ),
                (
                    "notifications_enable",
                    models.BooleanField(
                        default=False, verbose_name="Отправлять уведомления"
                    ),
                ),
                (
                    "notifications_target",
                    multiselectfield.db.fields.MultiSelectField(
                        choices=[
                            ("decr", "Цена конкурента уменьшилась"),
                            ("incr", "Цена конкурента увеличилась"),
                        ],
                        max_length=20,
                        null=True,
                        verbose_name="Цель уведомления",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор задачи",
                    ),
                ),
                (
                    "products",
                    models.ManyToManyField(
                        blank=True,
                        null=True,
                        related_name="tasks",
                        to="products.product",
                    ),
                ),
            ],
        ),
    ]
