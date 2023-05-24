from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'client',
        'salon',
        'master',
        'service',
        'time',
        'cost',
    )
    list_filter = ['salon', 'master', 'service']