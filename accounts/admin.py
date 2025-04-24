from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'subscription_active', 'subscription_end')

    list_filter = ('is_staff', 'is_superuser', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Подписка', {'fields': ('subscription_active', 'subscription_end')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)