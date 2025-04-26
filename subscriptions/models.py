from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings

from recipes.models import Recipe


class Subscription(models.Model):
    """Модель подписки пользователя."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    
    MENU_TYPE_CHOICES = [
        ('classic', 'Классическое'),
        ('low', 'Низкоуглеводное'),
        ('veg', 'Вегетарианское'),
        ('keto', 'Кето'),
    ]
    
    menu_type = models.CharField(
        _('Тип меню'),
        max_length=50,
        choices=MENU_TYPE_CHOICES
    )

    DURATION_CHOICES = [
        (1, '1 месяц'),
    ]

    duration = models.PositiveSmallIntegerField(
        _('Срок подписки'),
        choices=DURATION_CHOICES,
        default=1
    )
    
    # Выбранные приемы пищи
    include_breakfast = models.BooleanField(_('Завтраки'), default=True)
    include_lunch = models.BooleanField(_('Обеды'), default=True)
    include_dinner = models.BooleanField(_('Ужины'), default=True)
    include_dessert = models.BooleanField(_('Десерты'), default=True)
    
    # Количество персон
    persons_count = models.PositiveSmallIntegerField(_('Количество персон'), default=1)
    
    # Аллергены, которые нужно исключить
    exclude_fish = models.BooleanField(_('Исключить рыбу и морепродукты'), default=False)
    exclude_meat = models.BooleanField(_('Исключить мясо'), default=False)
    exclude_grains = models.BooleanField(_('Исключить зерновые'), default=False)
    exclude_honey = models.BooleanField(_('Исключить продукты пчеловодства'), default=False)
    exclude_nuts = models.BooleanField(_('Исключить орехи и бобовые'), default=False)
    exclude_dairy = models.BooleanField(_('Исключить молочные продукты'), default=False)
    
    # Даты начала и окончания подписки
    start_date = models.DateField(_('Дата начала'), default=timezone.now)
    end_date = models.DateField(_('Дата окончания'))
    
    # Статус подписки
    is_active = models.BooleanField(_('Активна'), default=True)
    
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
    
    def save(self, *args, **kwargs):
        # Рассчитываем дату окончания подписки при сохранении
        if not self.end_date:
            # Для простоты считаем, что в месяце 30 дней
            self.end_date = self.start_date + timezone.timedelta(days=30 * self.duration)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.get_menu_type_display()} подписка для {self.user.username}"
    
    class Meta:
        verbose_name = _('Подписка')
        verbose_name_plural = _('Подписки') 