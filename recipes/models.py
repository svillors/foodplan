from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Ingredient(models.Model):
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

    def __str__(self):
        return f'продукт {self.name}'

    def base_factor(self):
        """
        если грамм/миллилитр то = 1000
        если шт то = 1
        если упаковка то = 1
        """
        return 1000 if self.unit in ("g", "ml") else 1

    def price_for(self, quantity):
        return quantity / self.base_factor() * self.price_per_unit

    def calories_for(self, quantity):
        return quantity / self.base_factor() * self.calories_per_unit


class Tag(models.Model):
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

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Recipe(models.Model):
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

    def __str__(self):
        return f'Рецепт {self.name}'

    @property
    def total_calories(self):
        items = self.ingredientitem_set.select_related("ingredient")
        return sum(item.calories for item in items)

    @property
    def total_price(self):
        items = self.ingredientitem_set.select_related("ingredient")
        return sum(item.price for item in items)


class IngredientItem(models.Model):
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
    def calories(self):
        return self.ingredient.calories_for(self.quantity)

    @property
    def price(self):
        return self.ingredient.price_for(self.quantity)


class DailyMenu(models.Model):
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
