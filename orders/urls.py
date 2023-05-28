from django.urls import path

from orders.views import MakeOrder, OrderDetails,  payment

urlpatterns = [
    path(
        'configure/',
        MakeOrder.as_view(),
        name='configure_order'
    ),
    path(
        'configure/<int:master_id>/',
        MakeOrder.as_view(),
        name='master_order'
    ),
    path(
        '<int:order_id>/',
        OrderDetails.as_view(),
        name='order'
    ),
    path(
        'pay/<int:order_id>/',
        payment,
        name='pay'
    )

]
