# Generated by Django 4.1.7 on 2023-05-25 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salon',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='service',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
