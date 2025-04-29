from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    """Кастомизированная админ-панель для модели CustomUser.
    Attributes:
        model (Model): Связанная модель пользователя
        add_form (Form): Форма для создания новых пользователей
        list_display (Tuple): Поля для отображения в списке
        list_filter (Tuple): Поля для фильтрации в правой панели
        fieldsets (Tuple): Группировка полей в форме редактирования
        add_fieldsets (Tuple): Поля в форме создания пользователя
        search_fields (Tuple): Поля для поиска по тексту
        ordering (Tuple): Параметры сортировки по умолчанию
    """
    model = CustomUser
    add_form = CustomUserCreationForm

    list_display = ('email', 'first_name', 'is_active', 'subscription_active', 'subscription_end')

    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        ('Персональная информация', {'fields': ('first_name',  'email', 'password')}),
        ('Права доступа', {'fields': ('is_active', 'is_superuser')}),
        ('Подписка', {'fields': ('subscription_active', 'subscription_end', 'prefers')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name'),
        }),
    )

    search_fields = ('email', 'first_name')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)