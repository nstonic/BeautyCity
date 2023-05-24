from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from .models import Salon, Service


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['salons'] = Salon.objects.all()
        context['services'] = Service.objects.all()

        return context
