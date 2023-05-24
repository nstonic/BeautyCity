from django.contrib import admin
from .models import Service, Salon


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
    )


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'address',
    )
