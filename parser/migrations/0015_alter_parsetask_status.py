# Generated by Django 4.2.5 on 2023-09-12 11:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("parser", "0014_remove_parsetask_is_urls_valid_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="parsetask",
            name="status",
            field=models.IntegerField(
                choices=[
                    (1, "Создана"),
                    (2, "В работе"),
                    (3, "Отменена"),
                    (4, "Пауза"),
                    (5, "Остановлена"),
                    (6, "Настройка"),
                    (7, "Ошибка"),
                ],
                default=1,
                verbose_name="Статус",
            ),
        ),
    ]
