from .models import CustomUser  
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailInput


class CustomUserCreationForm(UserCreationForm):
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
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Фамилия"
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
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
        }