from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        salons = [
            {
                'name': 'Beauty city Пушкинская',
                'address': 'ул. Пушкинская, д. 78А',
                'photo': {'url': 'img/salons/salon1.svg'},
            },
            {
                'name': 'Beauty city Ленина',
                'address': 'ул. Ленина, д. 211',
                'photo': {'url': 'img/salons/salon2.svg'},
            },
            {
                'name': 'Beauty city Московская',
                'address': 'ул. Московская, д. 67',
                'photo': {'url': 'img/salons/salon3.svg'},
            },
        ]
        context['salons'] = salons
        return context
