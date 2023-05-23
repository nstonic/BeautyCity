from django.views.generic import TemplateView


# from services.models import Salon, Service, Master


class MakeOrder(TemplateView):
    template_name = 'service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # salons = Salon.objects.all()
        # services = Service.objects.all()
        # masters = Master.objects.all()
        masters = [
            {'name': 'Ольга',
             'salon': 'ул. Пушкинская, д. 78А'},
            {'name': 'Татьяна',
             'salon': 'ул. Пушкинская, д. 78А'}
        ]
        salons = [
            {'name': 'BeautyCity Пушкинская',
             'address': 'ул. Пушкинская, д. 78А'}
        ]
        services = [
            {'name': 'Мейкап',
             'price': 1000},
            {'name': 'Покраска волос',
             'price': 2000},
            {'name': 'Маникюр',
             'price': 3000}
        ]

        context.update({
            'masters': masters,
            'salons': salons,
            'services': services
        })
        return context
