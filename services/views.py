from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from .models import Salon, Service
from users.models import Master
from django.utils.timezone import localdate
from dateutil import relativedelta


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['salons'] = Salon.objects.all()
        context['services'] = Service.objects.all()

        masters = Master.objects.all()
        now = localdate()
        for master in masters:
            delta = relativedelta.relativedelta(now, master.experience_from)
            years = months = ''
            if delta.years:
                years = f'{delta.years} г.'
            if delta.months:
                months = f'{delta.months} мес.'
            master.experience = f'{years} {months}'
        context['masters'] = masters

        return context
