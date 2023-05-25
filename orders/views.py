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
            master_name = request.POST.get('master')
            salon_name = request.POST.get('salon')
            service_name = request.POST.get('service')
            master = Master.objects.get(name=master_name)
            salon = Salon.objects.get(name=salon_name)
            service = Service.objects.get(name=service_name)
            client = Client.objects.get(pk='+12125552368')
            Order.objects.create(
                salon=salon,
                master=master,
                service=service,
                client=client,
                time=now(),
                cost=service.price
            )
        return redirect('configure_order')
