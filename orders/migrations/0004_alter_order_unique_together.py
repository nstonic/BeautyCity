# Generated by Django 4.1.7 on 2023-05-25 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_master_portrait'),
        ('orders', '0003_order_created_at'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='order',
            unique_together={('master', 'time')},
        ),
    ]
