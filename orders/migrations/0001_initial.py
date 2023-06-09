# Generated by Django 4.1.7 on 2023-05-24 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('services', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(verbose_name='Order Time')),
                ('cost', models.IntegerField(verbose_name='Order Cost')),
                ('comment', models.TextField(blank=True, max_length=300, null=True, verbose_name='Order Comment')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='users.client', verbose_name='Order Client')),
                ('master', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='users.master', verbose_name='Order Master')),
                ('salon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='services.salon', verbose_name='Order Salon')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='services.service', verbose_name='Order Service')),
            ],
        ),
    ]
