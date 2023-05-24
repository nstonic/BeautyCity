from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from services.models import Service, Salon


class Client(models.Model):
    name = models.CharField(max_length=50, verbose_name='Client Name')
    phone_number = PhoneNumberField(verbose_name='Phone Number', unique=True)

    def __str__(self):
        return f'{self.name} {self.phone_number}'


class Master(models.Model):
    name = models.CharField(max_length=50, verbose_name='Master Name')
    service = models.ManyToManyField(Service, verbose_name='Master Services', related_name='masters')
    salon = models.ForeignKey(Salon, on_delete=models.SET_NULL, verbose_name='Master Salon', related_name='master', null=True)
    experience_from = models.DateField(null=True, blank=True)
    portrait = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}'
