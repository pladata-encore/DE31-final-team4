# Generated by Django 5.1 on 2024-09-05 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0004_alter_oncetime_ma120_alter_oncetime_ma20_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_name', models.CharField(max_length=50)),
                ('current_point', models.FloatField()),
                ('up_down_point', models.FloatField()),
                ('up_down_rate', models.FloatField()),
                ('up_down_flag', models.IntegerField()),
                ('price_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'market',
                'ordering': ['-price_time'],
            },
        ),
    ]
