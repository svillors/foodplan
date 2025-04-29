from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from typing import Any, Optional


class CustomUserManager(BaseUserManager):
    """Кастомный менеджер для модели пользователя с аутентификацией по email.

    Переопределяет стандартные методы создания пользователя и суперпользователя,
    заменяя поле username на email в качестве основного идентификатора.

    Attributes:
        use_in_migrations (bool): Флаг использования в миграциях (True)
    """
    use_in_migrations = True

    def create_user(
        self,
        email: str,
        password: Optional[str] = None,
        **extra_fields: Any
    ) -> models.Model:
        """Создает и сохраняет обычного пользователя с заданным email и паролем.

        Args:
            email (str): Обязательный email пользователя
            password (Optional[str]): Пароль пользователя (может быть None)
            **extra_fields: Дополнительные поля модели пользователя

        Returns:
            models.Model: Созданный объект пользователя

        Raises:
            ValueError: Если email не указан
        """
        if not email:
            raise ValueError('Необходимо указать адрес электронной почты')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: Optional[str] = None,
        **extra_fields: Any
    ) -> models.Model:
        """Создает суперпользователя с расширенными правами доступа.

        Args:
            email (str): Обязательный email пользователя
            password (Optional[str]): Пароль пользователя
            **extra_fields: Дополнительные поля модели пользователя

        Returns:
            models.Model: Созданный объект суперпользователя

        Raises:
            ValueError: Если не установлены флаги is_staff или is_superuser
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('У суперпользователя должно быть значение is_staff = True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('У суперпользователя должно быть значение is_superuser = True.')

        return self.create_user(email, password, **extra_fields)