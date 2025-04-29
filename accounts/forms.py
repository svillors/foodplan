from .models import CustomUser  
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailInput


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации пользователя с кастомными полями и стилями.

    Наследует стандартную форму UserCreationForm, добавляя:
    - Поля для email, имени
    - Кастомные CSS-классы и плейсхолдеры
    - Валидацию уникальности email
    - Стилизованные поля ввода паролей

    Attributes:
        password1 (CharField): Поле ввода пароля
        password2 (CharField): Поле подтверждения пароля
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')
        widgets = {
            "email": EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email",
                "id": "email",
                "name": "email"
            }),
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Имя"
            }),
        }
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "id": "password",
            "name": "password"
        })
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "id": "PasswordConfirm",
            "name": "password2"
        })
    )


class UserUpdateForm(forms.ModelForm):
    """Форма обновления данных пользователя с ограниченными полями.

    Позволяет изменять:
    - Имя
    - Email (только для отображения, редактирование отключено)

    Attributes:
        Meta.model (CustomUser): Связанная модель пользователя
        Meta.fields (tuple): Доступные для редактирования поля
        Meta.widgets (dict): Кастомизация виджетов полей
    """
    class Meta:
        model = CustomUser
        fields = ('first_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
        }