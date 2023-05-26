import phonenumbers
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.datetime_safe import datetime
from django.views.generic import TemplateView

from orders.forms import OrderForm, ClientForm
from orders.models import Order
from services.models import Salon, Service
from users.models import Master, Client


class OrderFinally(TemplateView):
    template_name = 'serviceFinally.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = kwargs.get('order_id')
        order = Order.objects.filter(pk=order_id).first()
        if order:
            order_time = order.time.strftime('%H:%M')
            order_date = order.time.strftime('%d %B')
            context.update({
                'order': order,
                'order_time': order_time,
                'order_date': order_date
            })
        return context

    def post(self, *args, **kwargs):
        order_id = self.request.POST.get('order_id')
        input_phone_number = self.request.POST.get('phone_number')
        comment = self.request.POST.get('comment')
        if input_phone_number.startswith('8'):
            input_phone_number = input_phone_number.replace('8', '+7', 1)
        phone_number = phonenumbers.parse(input_phone_number, 'ru')
        if phonenumbers.is_valid_number(phone_number):
            client_form = ClientForm(self.request.POST)
            client = Client.objects.filter(pk=input_phone_number).first()
            if not client:
                if client_form.is_valid():
                    client = client_form.save()
                else:
                    print(client_form.errors)
                    return redirect('index')
            order = get_object_or_404(Order, pk=order_id)
            order.client = client
            order.comment = comment
            order.save()
            return redirect('index')


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
        if master_id := kwargs.get('master_id'):
            context.update({
                'master': Master.objects.filter(pk=master_id).first()
            })
        return context

    def post(self, request, *args, **kwargs):
        input_form = self.get_input_form(
            self.request.POST
        )
        order_form = OrderForm(input_form)
        if order_form.is_valid():
            order = order_form.save()
            return redirect('final_order', order_id=order.pk)
        else:
            context = self.get_context_data(**kwargs)
            context.update({
                'form': order_form
            })
            return render(
                self.request,
                self.template_name,
                context,
            )

    @staticmethod
    def get_input_form(input_form):
        form = input_form.copy()
        date_input = form.get('date')
        time_input = form.get('time')
        if date_input and time_input:
            date = datetime.strptime(date_input, '%a, %d %b %Y %H:%M:%S %Z')
            time = datetime.strptime(time_input, '%H:%M')
            form['time'] = date.replace(hour=time.hour, minute=time.minute, second=0)
        if service_id := form.get('service'):
            service = Service.objects.get(pk=service_id)
            form['cost'] = service.price
        else:
            form['cost'] = 0
        return form
