from django.shortcuts import redirect, render
from django.utils.datetime_safe import datetime
from django.views.generic import TemplateView

from orders.forms import OrderForm
from orders.models import Order
from services.models import Salon, Service
from users.models import Master, Client


def order_final(request, order_id):
    return render(request, 'serviceFinally.html')


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
                'form': order_form,
                'non_field_errors': order_form.non_field_errors
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
