from django.urls import path

from orders.views import MakeOrder

urlpatterns = [
    path('configure', MakeOrder.as_view(), name='configure_order')
]
