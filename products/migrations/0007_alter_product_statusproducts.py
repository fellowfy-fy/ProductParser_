# Generated by Django 4.2.5 on 2024-03-19 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_remove_productpricehistory_statusproducts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='statusproducts',
            field=models.ManyToManyField(blank=True, null=True, related_name='products', to='products.statusproduct'),
        ),
    ]
