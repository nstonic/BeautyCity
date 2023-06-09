# Generated by Django 4.1.7 on 2023-05-26 11:30

from django.db import migrations, models
import orders.models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.DateTimeField(validators=[orders.models.time_not_past, orders.models.time_is_half_hour_interval], verbose_name='Order Time'),
        ),
    ]
