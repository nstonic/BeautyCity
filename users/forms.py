from django.forms import ModelForm

from users.models import Client


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone_number', ]
        labels = {
            'name': 'Имя',
            'phone_number': 'Номер телефона',
        }
