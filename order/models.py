from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    MENU_TYPES = [
        ('classic', 'Классическое'),
        ('low', 'Низкоуглеводное'),
        ('veg', 'Вегетарианское'),
        ('keto', 'Кето'),
    ]
    menu_type = models.CharField(
        'Тип меню',
        max_length=20,
        choices=MENU_TYPES
    )
    duration = models.PositiveSmallIntegerField('Срок (месяцев)')
    include_breakfast = models.BooleanField('Завтраки', default=True)
    include_lunch = models.BooleanField('Обеды', default=True)
    include_dinner = models.BooleanField('Ужины', default=True)
    include_dessert = models.BooleanField('Десерты', default=True)
    persons = models.PositiveSmallIntegerField('Количество персон', default=1)
    allergies = models.ManyToManyField(
        'Allergy',
        verbose_name='Аллергии',
        blank=True
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    STATUS_CHOICES = [
        ('created', 'Создан'),
        ('paid', 'Оплачен'),
        ('cancelled', 'Отменён'),
    ]
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='created'
    )
    subscription = models.ForeignKey('subscriptions.Subscription', on_delete=models.CASCADE, null=True, blank=True)
    is_paid = models.BooleanField('Оплачен', default=False)


class Allergy(models.Model):
    name = models.CharField('Название', max_length=100)

    def __str__(self):
        return self.name