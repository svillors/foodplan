from django.db import models


class Ingredient(models.Model):
    UNIT_CHOICES = [("g", "г"), ("ml", "мл"), ("pcs", "шт")]
    name = models.CharField(
        'Название',
        max_length=60
    )
    unit = models.CharField(
        max_length=3,
        choices=UNIT_CHOICES
    )
    price_per_unit = models.FloatField(
        'Цена на еденицу измерения'
    )
    calories_per_unit = models.FloatField(
        'Калории на еденицу измерения'
    )

    def __str__(self):
        return f'продукт {self.name}'

    def base_factor(self):
        """
        если грамм/миллилитр то = 100
        если шт то = 1
        """
        return 100 if self.unit in ("g", "ml") else 1

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

    def __str__(self):
        return self.name


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
        null=True
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
