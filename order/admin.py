from django.contrib import admin

from .models import Order, Allergy

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'menu_type', 'duration', 'is_paid']

@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    pass