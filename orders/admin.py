from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'is_active',
        'is_paid',
        'created_at',
        'client',
        'salon',
        'master',
        'service',
        'time',
        'cost',
    )
    fields = [
        'is_active',
        'is_paid',
        'client',
        'salon',
        'master',
        'service',
        'time',
        'comment',
        'cost',
        'created_at'
    ]
    readonly_fields = [
        'id',
        'is_active',
        'created_at',
        'cost'
    ]
    list_filter = ['salon', 'master', 'service']

    def save_form(self, request, form, change):
        instance = form.save(commit=False)
        if not instance.client:
            instance.is_active = False
        else:
            instance.is_active = True
        if not instance.cost:
            instance.cost = instance.service.price
        return form.save(commit=False)
