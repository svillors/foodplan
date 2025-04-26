from django.contrib import admin

from .models import Order, Allergy

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'menu_type', 'duration', 'is_paid']
    # list_display = ('id', 'user', 'is_paid', 'created_at')
    list_filter = ('is_paid',)
    

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     # Показываем только оплаченные заказы
    #     return qs.filter(is_paid=True)

@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    pass

