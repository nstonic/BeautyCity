from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=50, verbose_name='Service Name')
    price = models.IntegerField(verbose_name='Service Price')
    photo = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class Salon(models.Model):
    name = models.CharField(max_length=50, verbose_name='Salon Name')
    address = models.CharField(max_length=100, verbose_name='Salon Address')
    photo = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}'
