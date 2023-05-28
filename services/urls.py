from django.urls import path

from .views import Index, contacts

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('contacts/', contacts, name='contacts')
]
