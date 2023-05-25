from django.urls import path

from orders.views import MakeOrder, order_final

urlpatterns = [
    path('configure', MakeOrder.as_view(), name='configure_order'),
    path('final', order_final, name='final_order')
]
