from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm

from orders.models import Order
from users.models import Client


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['salon', 'master', 'service', 'time', 'cost']
        labels = {
            'salon': 'Салон',
            'master': 'Мастер',
            'service': 'Услуга',
            'time': 'Дата и время'
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': 'К сожалению мастер в это время занят',
            }
        }


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone_number']
        labels = {
            'name': 'Имя',
            'phone_number': 'Номер телефона'
        }
