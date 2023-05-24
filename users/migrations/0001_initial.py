# Generated by Django 4.1.7 on 2023-05-24 15:37

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('name', models.CharField(max_length=50, verbose_name='Client Name')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, primary_key=True, region=None, serialize=False, verbose_name='Phone Number')),
            ],
        ),
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Master Name')),
                ('experience_from', models.DateField(blank=True, null=True)),
                ('portrait', models.ImageField(blank=True, null=True, upload_to='')),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('salon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='master', to='services.salon', verbose_name='Master Salon')),
                ('service', models.ManyToManyField(related_name='masters', to='services.service', verbose_name='Master Services')),
            ],
        ),
    ]
