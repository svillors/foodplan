from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Административный интерфейс для управления заказами.

    Attributes:
        list_display (list): Отображаемые поля в списке заказов:
            - user: Пользователь
            - menu_type: Выбранный тип меню
            - duration: Срок подписки (месяцы)
            - is_paid: Статус оплаты
        list_filter (tuple): Фильтрация по полю is_paid
    """
    list_display = ['user', 'menu_type', 'duration', 'is_paid']
    list_filter = ('is_paid',)
