from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Allergy(models.Model):
    """Модель аллергенов.

    Attributes:
        name (CharField): Название аллергена. Максимальная длина - 100 символов.

    Methods:
        __str__(): Возвращает строковое представление названия аллергена.
    """
    name = models.CharField('Название', max_length=100)

    def __str__(self):
        return self.name


class Order(models.Model):
    """Модель заказа пользователя.

    Attributes:
        user (ForeignKey): Связь с пользователем. Каскадное удаление.
        prefers (ManyToManyField): Предпочтения в тегах рецептов.
        tags (ManyToManyField): Теги заказа с отдельным related_name.
        menu_type (CharField): Тип меню с предопределенными вариантами.
        duration (PositiveSmallIntegerField): Срок подписки в месяцах.
        include_* (BooleanField): Флаги включения приемов пищи.
        persons (PositiveSmallIntegerField): Количество персон.
        allergies (ManyToManyField): Связанные аллергены.
        created_at (DateTimeField): Дата создания с автоуказанием.
        is_paid (BooleanField): Статус оплаты.
        updated_at (DateTimeField): Дата изменения с автообновлением.
        menu_slug (CharField): Слаг меню для генерации URL.

    Methods:
        get_menu(): Формирует краткое описание меню.
        get_selected_meals(): Возвращает выбранные приемы пищи.
        get_menu_type_value(): Получает значение типа меню по имени тега.
    """
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    prefers = models.ManyToManyField(
        'recipes.Tag',
        verbose_name='Предпоч',
        blank=True,
    )
    tags = models.ManyToManyField(
        'recipes.Tag',
        verbose_name='Теги',
        blank=True,
        related_name='orders_tags'
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
        null=True, blank=True
    )
    include_breakfast = models.BooleanField('Завтраки', default=True)
    include_lunch = models.BooleanField('Обеды', default=True)
    include_dinner = models.BooleanField('Ужины', default=True)
    include_dessert = models.BooleanField('Десерты', default=True)
    persons = models.PositiveSmallIntegerField('Количество персон', default=1, null=True, blank=True)
    allergies = models.ManyToManyField(
        Allergy,
        verbose_name='Предпочтения',
        blank=True
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_paid = models.BooleanField('Оплачен', default=False)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True) 
    menu_slug = models.CharField(max_length=50, blank=True, null=True)

    def get_menu(self) -> str:
        """Формирует строку с типом меню и количеством персон."""
        return f"Меню: {self.menu_type}, Персон: {self.persons}"

    def get_selected_meals(self) -> str:
        """Возвращает список выбранных приемов пищи через запятую."""
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

    def get_menu_type_value(self, menu_types: list[tuple[str, str]]) -> str | None:
        """Находит значение типа меню по имени связанного тега.

        Args:
            menu_types: Список кортежей (значение, название) типов меню

        Returns:
            str: Значение типа меню или None при отсутствии совпадений
        """
        for value, name in menu_types:
            if name == self.menu_tag.name:
                return value
        return None
