# Generated by Django 5.1 on 2024-09-03 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_datawarehouse'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='datawarehouse',
            table='dictionary',
        ),
    ]
