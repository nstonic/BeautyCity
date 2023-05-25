from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm

from orders.models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['salon', 'master', 'service', 'client', 'time']
        labels = {
            'salon': 'Салон',
            'master': 'Мастер',
            'service': 'Услуга',
            'client': 'Клиент',
            'time': 'Дата и время'
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': 'К сожалению мастер в это время занят',
            }
        }

    def save(self, commit=True):
        self.instance.time = self.cleaned_data.get('time')
        self.instance.cost = self.cleaned_data['service'].price
        super().save(commit=True)
