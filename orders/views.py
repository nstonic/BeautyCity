import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views.generic import TemplateView

from orders.forms import OrderForm
from orders.models import Order
from services.models import Salon, Service
from users.forms import ClientForm
from users.models import Client, Master


class OrderDetails(TemplateView):
    template_name = 'serviceFinally.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = kwargs.get('order_id')
        order = Order.objects.select_related('salon') \
            .select_related('service') \
            .select_related('master') \
            .get(id=order_id)
        if stripe_session_id := self.request.GET.get('stripe_session_id'):
            stripe_session = stripe.checkout.Session.retrieve(
                stripe_session_id)
            if stripe_session.payment_status == 'paid':
                order.is_paid = True
                order.save()
        context['order'] = order
        return context

    def post(self, request, *args, **kwargs):
        input_form = self.request.POST
        client_form = None
        client = Client.objects.filter(
            phone_number=input_form['phone_number']
        ).first()
        if not client:
            client_form = ClientForm(input_form)
        else:
            if client.name != input_form['name']:
                client_form = ClientForm(input_form, instance=client)

        if client_form:
            if client_form.is_valid():
                client = client_form.save()
            else:
                context = self.get_context_data(**kwargs)
                context.update(
                    {
                        'form': client_form,
                        'client_name': input_form['name'],
                        'client_phone_number': input_form['phone_number'],
                        'client_question': input_form['question'],
                    }
                )
                return render(
                    self.request,
                    self.template_name,
                    context,
                )

        order_id = kwargs['order_id']
        Order.objects.filter(id=order_id).update(
            client=client,
            active=True,
            comment=input_form['question'],
        )

        return redirect('order', order_id=order_id)


class MakeOrder(TemplateView):
    template_name = 'service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'masters': Master.objects.all(),
            'salons': Salon.objects.all(),
            'services': Service.objects.all()
        })
        if master_id := kwargs.get('master_id'):
            context.update({
                'current_master': Master.objects.filter(
                    pk=master_id
                ).first()
            })
        return context

    def post(self, request, *args, **kwargs):
        input_form = self.get_input_form()
        order_form = OrderForm(input_form)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.active = False
            order.save()
            return redirect('order', order_id=order.pk)
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = order_form
            if service := order_form.cleaned_data.get('service'):
                context['current_service'] = service
            if master := order_form.cleaned_data.get('master'):
                context['current_master'] = master
            if salon := order_form.cleaned_data.get('salon'):
                context['current_salon'] = salon
            return render(
                self.request,
                self.template_name,
                context,
            )

    def get_input_form(self):
        form = self.request.POST.copy()
        date_input = form.get('date')
        time_input = form.get('time')
        form['active'] = True
        if date_input and time_input:
            date = datetime.strptime(date_input, '%a %b %d %Y')
            time = datetime.strptime(time_input, '%H:%M')
            form['time'] = date.replace(
                hour=time.hour,
                minute=time.minute,
                second=0
            )
        if service_id := form.get('service'):
            service = get_object_or_404(Service, pk=service_id)
            form['cost'] = service.price
        else:
            form['cost'] = 0
        return form


def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    client = order.client
    if not client:
        return redirect('index')
    stripe.api_key = settings.STRIPE_SECRET_KEY
    response = stripe.Price.create(
        unit_amount=order.cost * 100,
        product=settings.BOX_STRIPE_ID,
        currency='rub'
    )
    price_id = response['id']
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price': price_id,
                'quantity': 1,
            },
        ],
        mode='payment',
        metadata={'client_id': client.pk, 'order_id': order.pk},
        success_url=settings.DOMAIN +
        reverse('order', kwargs={'order_id': order.pk}) +
        '?stripe_session_id={CHECKOUT_SESSION_ID}',
        cancel_url=settings.DOMAIN +
        reverse('order', kwargs={'order_id': order.pk}) +
        '?stripe_session_id={CHECKOUT_SESSION_ID}'
    )
    return redirect(checkout_session.url, code=303)
