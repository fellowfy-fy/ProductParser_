# Generated by Django 4.2.5 on 2023-09-06 07:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("parser", "0011_parsetask_name"),
        ("products", "0005_product_synonyms"),
    ]

    operations = [
        migrations.AddField(
            model_name="productpricehistory",
            name="task",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="parser.parsetask",
                verbose_name="Создано задачей",
            ),
        ),
    ]
