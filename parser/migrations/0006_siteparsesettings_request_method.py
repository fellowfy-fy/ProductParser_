# Generated by Django 4.2.5 on 2023-09-05 14:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("parser", "0005_siteparsesettings_parse_mode_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteparsesettings",
            name="request_method",
            field=models.CharField(
                choices=[("GET", "GET"), ("POST", "POST")],
                default="GET",
                max_length=5,
                verbose_name="HTTP метод",
            ),
        ),
    ]
