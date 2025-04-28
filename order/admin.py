from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'menu_type', 'duration', 'is_paid']
    list_filter = ('is_paid',)
