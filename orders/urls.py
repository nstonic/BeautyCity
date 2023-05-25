from django.urls import path

from orders.views import MakeOrder, order_final

urlpatterns = [
    path('configure', MakeOrder.as_view(), name='configure_order'),
    path('configure/<int:master_id>', MakeOrder.as_view(), name='master_order'),
    path('final/<int:order_id>', order_final, name='final_order')
]
