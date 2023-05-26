from django.db import models
from services.models import Service, Salon
from users.models import Client, Master
from django.utils import timezone
from django.core.exceptions import ValidationError


def time_not_past(time):
    if time < timezone.now():
        raise ValidationError('Нельзя оформить запись на прошедшую дату и время')


def time_is_half_hour_interval(time):
    if not time.minute in (0, 30):
        raise ValidationError('Недопустимое время. Запись производится диапазонами строго по 30 минут')


class Order(models.Model):
    salon = models.ForeignKey(Salon, verbose_name='Order Salon', related_name='orders', on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Client, verbose_name='Order Client', related_name='orders', on_delete=models.SET_NULL, null=True)
    master = models.ForeignKey(Master, verbose_name='Order Master', related_name='orders', on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(Service, verbose_name='Order Service', related_name='orders', on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField(verbose_name='Order Time', validators=[time_not_past, time_is_half_hour_interval])
    cost = models.IntegerField(verbose_name='Order Cost')
    comment = models.TextField(verbose_name='Order Comment', max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        unique_together = ['master', 'time']

    def __str__(self):
        return f'{self.master} - {self.service}, {self.time}'
