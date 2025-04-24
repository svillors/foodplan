from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    subscription_active = models.BooleanField(verbose_name='Начало подписки', default=False)
    subscription_end = models.DateField(verbose_name='Конец подписки', null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    first_name = models.CharField(verbose_name='Имя', max_length=150, blank=True)