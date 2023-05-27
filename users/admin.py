from django.contrib import admin
from .models import Client, Master, Review


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


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'master',
        'client',
        'rating',
        'created_at'
    )