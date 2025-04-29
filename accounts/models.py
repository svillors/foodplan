from django.contrib.auth.models import AbstractUser
from django.db import models
from typing import Optional, List
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """Кастомная модель пользователя с аутентификацией по email и расширенными полями.

    Заменяет стандартную модель пользователя Django, добавляя:
    - Аутентификацию по email вместо username
    - Систему подписки с датой окончания
    - Пищевые предпочтения через теги
    - Аватар пользователя
    - Кастомный менеджер объектов

    Attributes:
        email (models.EmailField): Уникальный email пользователя (используется для входа)
        subscription_active (models.BooleanField): Флаг активности подписки
        subscription_end (models.DateField): Дата окончания подписки
        prefers (models.ManyToManyField): Связанные теги предпочтений
        avatar (models.ImageField): Загружаемый аватар пользователя
        first_name (models.CharField): Имя для персонального обращения
    """
    username = None
    email = models.EmailField(unique=True, blank=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    subscription_active = models.BooleanField(
        verbose_name='Активна ли подписка',
        default=False
    )
    subscription_end = models.DateField(
        verbose_name='Конец подписки',
        null=True,
        blank=True
    )
    prefers = models.ManyToManyField(
        'recipes.Tag',
        verbose_name='Предпочтения',
        blank=True,
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True
    )
