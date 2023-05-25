from django.shortcuts import redirect
from django.utils.datetime_safe import datetime
from django.views.generic import TemplateView

from orders.forms import OrderForm
from orders.models import Order
from services.models import Salon, Service
from users.models import Master, Client


class MakeOrder(TemplateView):
    template_name = 'service.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context.update({
            'masters': Master.objects.all(),
            'salons': Salon.objects.all(),
            'services': Service.objects.all(),
            'orders': Order.objects.all()
        })
        return context

    def post(self, request, *args, **kwargs):
        cleaned_input_form = self._clean_input_order_form(
            self.request.POST.copy()
        )
        Client.objects.get_or_create(
            phone_number=cleaned_input_form.get('client'),
            defaults={'name': 'Вася'}
        )
        order_form = OrderForm(cleaned_input_form)
        if order_form.is_valid():
            order_form.save()
        else:
            print(order_form.errors)
        return redirect('configure_order')

    @staticmethod
    def _clean_input_order_form(input_form):
        phone_number = input_form.get('client')
        if phone_number.startswith('8'):
            input_form['client'] = phone_number.replace('8', '+7', 1)
        date = input_form['date']
        if date:
            input_form['date'] = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
        return input_form
