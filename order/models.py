from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Allergy(models.Model):
    name = models.CharField('Название', max_length=100)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    prefers = models.ManyToManyField(
        'recipes.Tag',
        verbose_name='Предпоч',
        blank=True
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
        choices=MENU_TYPES,
        null=False,
        blank=False
    )
    duration = models.PositiveSmallIntegerField(
        'Срок (месяцев)', 
        default=1,
    )
    include_breakfast = models.BooleanField('Завтраки', default=True)
    include_lunch = models.BooleanField('Обеды', default=True)
    include_dinner = models.BooleanField('Ужины', default=True)
    include_dessert = models.BooleanField('Десерты', default=True)
    persons = models.PositiveSmallIntegerField('Количество персон', default=1)
    allergies = models.ManyToManyField(
        Allergy,
        verbose_name='Предпочтения',
        blank=True
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_paid = models.BooleanField('Оплачен', default=False)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True) 

    def get_menu(self):
        return f"Меню: {self.menu_type}, Персон: {self.persons}"

    def get_selected_meals(self):
        meals = []
        if self.include_breakfast: 
            meals.append('Завтраки')
        if self.include_lunch: 
            meals.append('Обеды')
        if self.include_dinner: 
            meals.append('Ужины')
        if self.include_dessert: 
            meals.append('Десерты')
        return ', '.join(meals)