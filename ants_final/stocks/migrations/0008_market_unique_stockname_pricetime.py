# Generated by Django 5.1 on 2024-09-06 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0007_remove_market_unique_stockname_pricetime_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='market',
            constraint=models.UniqueConstraint(fields=('StockName', 'price_time'), name='unique_stockname_pricetime'),
        ),
    ]
