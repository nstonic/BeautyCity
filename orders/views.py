import stripe
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views.generic import TemplateView

from orders.forms import OrderForm
from orders.models import Order
from services.models import Salon, Service
from users.models import Master, Client
from users.forms import ClientForm


class OrderFinally(TemplateView):
    template_name = 'serviceFinally.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = kwargs.get('order_id')
        order = Order.objects.select_related('salon') \
            .select_related('service') \
            .select_related('master') \
            .get(id=order_id)
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
                kwargs['client_name'] = input_form['name']
                kwargs['client_phone_number'] = input_form['phone_number']
                kwargs['client_question'] = input_form['question']
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

        return redirect('accepted_order', order_id=order_id)


class AcceptedOrder(TemplateView):
    template_name = 'accepted_order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = kwargs.get('order_id')
        order = Order.objects.select_related('salon') \
            .select_related('service') \
            .select_related('master') \
            .get(id=order_id)
        context['order'] = order
        return context


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
            order = order_form.save(commit=False)
            order.active = False
            order.save()
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
        form['active'] = True
        if date_input and time_input:
            date = datetime.strptime(date_input, '%a %b %d %Y')
            time = datetime.strptime(time_input, '%H:%M')
            form['time'] = date.replace(
                hour=time.hour, minute=time.minute, second=0)
        if service_id := form.get('service'):
            service = Service.objects.get(pk=service_id)
            form['cost'] = service.price
        else:
            form['cost'] = 0
        return form


def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    client = order.client
    if not client:
        return redirect('index')
    return create_checkout_session(client, order)


def create_checkout_session(client, order):
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
                    reverse('paid_order', kwargs={'order_id': order.pk}) +
                    '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=settings.DOMAIN +
                   reverse('paid_order', kwargs={'order_id': order.pk}) +
                   '?session_id={CHECKOUT_SESSION_ID}'
    )
    return redirect(checkout_session.url, code=303)


class PaidOrder(TemplateView):
    template_name = 'paid.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = kwargs.get('order_id')
        order = Order.objects.select_related('salon') \
            .select_related('service') \
            .select_related('master') \
            .get(id=order_id)
        if session_id := self.request.GET.get('session_id'):
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid':
                order.is_paid = True
                order.save()
        context['order'] = order
        return context
