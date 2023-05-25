from django.shortcuts import redirect
from django.utils.timezone import now
from django.views.generic import TemplateView

from orders.forms import OrderForm
from orders.models import Order
from services.models import Salon, Service
from users.models import Master, Client


class MakeOrder(TemplateView):
    template_name = 'service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        salons = Salon.objects.all()
        services = Service.objects.all()
        masters = Master.objects.all()

        context.update({
            'masters': masters,
            'salons': salons,
            'services': services
        })
        return context

    def post(self, request, *args, **kwargs):

        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_form.save()
            # Order.objects.create(
            #     salon=order_form.cleaned_data['salon'],
            #     service=order_form.cleaned_data['service'],
            #     master=order_form.cleaned_data['master'],
            #     client=order_form.cleaned_data['client'],
            #     time=now(),
            #     cost=order_form.cleaned_data['service'].price
            # )
        return redirect('configure_order')
