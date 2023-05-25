from django.forms import ModelForm

from orders.models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['salon', 'master', 'service', 'client', 'time']

    def save(self, commit=True):
        self.instance.time = self.cleaned_data.get('date')
        self.instance.cost = self.cleaned_data['service'].price
        super().save(commit=True)
