from .models import CustomUser  
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailInput


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email',)
        widgets = {
            "email": EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email",
                "id": "email",
                "name": "email"
            }),
        }

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "id": "password",
            "name": "password1"
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
