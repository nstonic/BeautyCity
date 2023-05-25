from django.forms import ModelForm
from django.utils.timezone import now

from orders.models import Order
from users.models import Client


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['salon', 'master', 'service', 'client']

    def clean(self):
        phone_number = self.data['client']
        if phone_number.startswith('8'):
            phone_number = phone_number.replace('8', '+7', 1)
            self.data['client'] = phone_number
        Client.objects.get_or_create(
            name='Вася',
            phone_number=phone_number
        )
        return super().clean()

    def save(self, commit=True):
        self.instance.time = now()
        self.instance.cost = self.cleaned_data['service'].price
        super().save(commit=True)
