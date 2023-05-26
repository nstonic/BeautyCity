from django.urls import path

from orders.views import MakeOrder, OrderFinally

urlpatterns = [
    path('configure', MakeOrder.as_view(), name='configure_order'),
    path('configure/<int:master_id>', MakeOrder.as_view(), name='master_order'),
    path('final/<int:order_id>', OrderFinally.as_view(), name='final_order')
]
