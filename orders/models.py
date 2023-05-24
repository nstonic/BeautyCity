from django.db import models
from services.models import Service, Salon
from users.models import Client, Master


class Order(models.Model):
    salon = models.ForeignKey(Salon, verbose_name='Order Salon', related_name='orders', on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Client, verbose_name='Order Client', related_name='orders', on_delete=models.SET_NULL, null=True)
    master = models.ForeignKey(Master, verbose_name='Order Master', related_name='orders', on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(Service, verbose_name='Order Service', related_name='orders', on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField(verbose_name='Order Time')
    cost = models.IntegerField(verbose_name='Order Cost')
    comment = models.TextField(verbose_name='Order Comment', max_length=300, blank=True, null=True)

    def __str__(self):
        return f'{self.master} - {self.service}, {self.time}'
