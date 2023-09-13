# Generated by Django 4.2.5 on 2023-09-13 13:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("parser", "0017_siteparsesettings_use_selenium_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteparsesettings",
            name="url_before",
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name="Посетить URL перед задачей"),
        ),
    ]
