from django.urls import path

from orders.views import MakeOrder, OrderFinally, AcceptedOrder, payment, PaidOrder

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
        'final/<int:order_id>/',
        OrderFinally.as_view(),
        name='final_order'
    ),
    path(
        'accepted_order/<int:order_id>/',
        AcceptedOrder.as_view(),
        name='accepted_order'
    ),
    path(
        'paid/<int:order_id>',
        PaidOrder.as_view(),
        name='paid_order'
    ),
    path(
        'pay/<int:order_id>',
        payment,
        name='pay'
    )

]
