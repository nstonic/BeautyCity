from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'active',
        'created_at',
        'client',
        'salon',
        'master',
        'service',
        'time',
        'cost',
    )
    readonly_fields = [
        'id',
        'created_at',
        'cost'
    ]
    list_filter = ['salon', 'master', 'service']

    def save_form(self, request, form, change):
        instance = form.save(commit=False)
        if not instance.cost:
            instance.cost = instance.service.price
        return form.save(commit=False)
