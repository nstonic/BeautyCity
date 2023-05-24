from django.contrib import admin
from .models import Client, Master


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'phone_number',
    )

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'salon',
        'experience_from',
    )
