from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Ingredient(models.Model):
    """Модель ингредиентов для рецептов.

    Attributes:
        name (CharField): Название ингредиента (до 60 символов)
        unit (CharField): Единица измерения (g/ml/pcs/pkg)
        price_per_unit (FloatField): Цена за базовую единицу
        calories_per_unit (FloatField): Калории за базовую единицу

    Methods:
        base_factor(): Возвращает коэффициент пересчета для единиц измерения
        price_for(quantity): Расчет стоимости для указанного количества
        calories_for(quantity): Расчет калорий для указанного количества
    """
    UNIT_CHOICES = [
        ("g", "г"),
        ("ml", "мл"),
        ("pcs", "шт"),
        ("pkg", "упаков")
    ]
    name = models.CharField(
        'Название',
        max_length=60
    )
    unit = models.CharField(
        max_length=3,
        choices=UNIT_CHOICES
    )
    price_per_unit = models.FloatField(
        'Цена на еденицу измерения',
        help_text='цена рассчтывается за 1 кг/литр или же за 1 шт/упаков'
    )
    calories_per_unit = models.FloatField(
        'Калории на еденицу измерения',
        help_text='калории рассчтываются за 1 кг/литр или же за 1 шт/упаков'
    )

    def __str__(self) -> str:
        return f'продукт {self.name}'

    def base_factor(self):
        """
        Возвращает коэффициент преобразования для единиц измерения.

        - если грамм/миллилитр то = 1000
        - если шт то = 1
        - если упаковка то = 1
        """
        return 1000 if self.unit in ("g", "ml") else 1

    def price_for(self, quantity: float) -> float:
        """Рассчитывает стоимость для указанного количества."""
        return quantity / self.base_factor() * self.price_per_unit

    def calories_for(self, quantity: float) -> float:
        """Рассчитывает калории для указанного количества."""
        return quantity / self.base_factor() * self.calories_per_unit


class Tag(models.Model):
    """Модель тегов для категоризации рецептов.

    Атрибуты:
        name (CharField): Уникальное название тега (до 50 символов)
        category (CharField): Категория тега (menu_type/food_intake/allergy)
    """
    name = models.CharField(
        'Название',
        max_length=50,
        unique=True
    )
    CATEGORIES = [
        ('menu_type', 'Тип меню'),
        ('food_intake', 'Приём пищи'),
        ('allergy', 'Аллергия'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORIES, default='food_intake')

    def __str__(self) -> str:
        return f"{self.name} ({self.get_category_display()})"


class Recipe(models.Model):
    """Модель рецептов с расчетом питательных свойств.

    Атрибуты:
        name (CharField): Название рецепта (до 60 символов)
        description (TextField): Подробное описание рецепта
        ingredients (ManyToManyField): Ингредиенты через промежуточную модель
        image (ImageField): Изображение готового блюда
        tags (ManyToManyField): Связанные теги

    Свойства:
        total_calories: Суммарная калорийность всех ингредиентов
        total_price: Общая стоимость всех ингредиентов
    """
    name = models.CharField(
        'Название',
        max_length=60
    )
    description = models.TextField(
        'Описание',
        blank=True
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientItem',
        verbose_name='Ингредиенты',
        related_name='recipes'
    )
    image = models.ImageField(
        'Картинка'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        blank=True,
    )

    def __str__(self) -> str:
        return f'Рецепт {self.name}'

    @property
    def total_calories(self) -> float:
        """Общая калорийность рецепта."""
        items = self.ingredientitem_set.select_related("ingredient")
        return sum(item.calories for item in items)

    @property
    def total_price(self) -> float:
        """Общая стоимость рецепта."""
        items = self.ingredientitem_set.select_related("ingredient")
        return sum(item.price for item in items)


class IngredientItem(models.Model):
    """Промежуточная модель для связи рецепта и ингредиентов.

    Атрибуты:
        recipe (ForeignKey): Связанный рецепт
        ingredient (ForeignKey): Используемый ингредиент
        quantity (FloatField): Количество ингредиента

    Свойства:
        calories: Калории для указанного количества
        price: Стоимость для указанного количества
    """
    recipe = models.ForeignKey(
        'Recipe',
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE
    )
    quantity = models.FloatField(
        'Количество'
    )

    @property
    def calories(self) -> float:
        """Рассчитанные калории для данного количества."""
        return self.ingredient.calories_for(self.quantity)

    @property
    def price(self) -> float:
        """Рассчитанная стоимость для данного количества."""
        return self.ingredient.price_for(self.quantity)


class DailyMenu(models.Model):
    """Модель дневного меню пользователя.

    Атрибуты:
        user (ForeignKey): Пользователь меню
        date (DateField): Дата меню
        recipes (ManyToManyField): Выбранные рецепты
        change_count (IntegerField): Лимит изменений меню

    Особенности:
        Уникальная комбинация пользователя и даты
    """
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    date = models.DateField(
        'Дата'
    )
    recipes = models.ManyToManyField(
        Recipe,
        verbose_name='Рецепты'
    )
    change_count = models.IntegerField(
        'Количество изменений блюд',
        default=3
    )

    class Meta:
        unique_together = ['user', 'date']
