from django.db import models
from services.models import Service, Salon
from users.models import Client, Master
from django.utils import timezone
from django.core.exceptions import ValidationError


def time_not_past(time):
    if time < timezone.now():
        raise ValidationError('Нельзя оформить запись на прошедшую дату и время')


def time_is_half_hour_interval(time):
    if time.minute not in (0, 30) or not time.second == 0:
        raise ValidationError('Недопустимое время. Запись производится диапазонами строго по 30 минут')


class Order(models.Model):
    active = models.BooleanField(verbose_name='Активен')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачен')
    salon = models.ForeignKey(Salon, verbose_name='Салон', related_name='orders', on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Client, verbose_name='Клиент', related_name='orders', on_delete=models.SET_NULL, null=True)
    master = models.ForeignKey(Master, verbose_name='Мастер', related_name='orders', on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(Service, verbose_name='Услуга', related_name='orders', on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField(verbose_name='Время записи', validators=[time_not_past, time_is_half_hour_interval])
    cost = models.IntegerField(verbose_name='Стоимость')
    comment = models.TextField(verbose_name='Комментарий', max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Создан')


    class Meta:
        unique_together = ['master', 'time', 'active']

    def __str__(self):
        return f'{self.master} - {self.service}, {self.time}'
