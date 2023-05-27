from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from services.models import Service, Salon


class Client(models.Model):
    name = models.CharField(max_length=50, verbose_name='Client Name', blank=True, null=True)
    phone_number = PhoneNumberField(verbose_name='Phone Number', primary_key=True, region='RU')

    def __str__(self):
        return f'{self.name} {self.phone_number}'


class Master(models.Model):
    name = models.CharField(max_length=50, verbose_name='Master Name')
    service = models.ManyToManyField(Service, verbose_name='Master Services', related_name='masters')
    salon = models.ForeignKey(Salon, on_delete=models.SET_NULL, verbose_name='Master Salon', related_name='master', null=True)
    experience_from = models.DateField(null=True, blank=True)
    portrait = models.FileField(blank=True, null=True)
    description = models.TextField(max_length=300, blank=True, null=True)
    specialty = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class Review(models.Model):
    client = models.ForeignKey(Client, verbose_name='Review Client', related_name='reviews', on_delete=models.CASCADE)
    master = models.ForeignKey(Master, verbose_name='Review Master', related_name='reviews', on_delete=models.CASCADE)
    rating = models.FloatField(
        verbose_name='Review Rating',
        choices=(
            (0, '0'),
            (0.5, '0.5'),
            (1, '1'),
            (1.5, '1.5'),
            (2, '2'),
            (2.5, '2.5'),
            (3, '3'),
            (3.5, '3.5'),
            (4, '4'),
            (4.5, '4.5'),
            (5, '5'),
        )
    )
    comment = models.TextField(max_length=300, verbose_name='Review Comment', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.master} - {self.rating}'
