from django.contrib import admin

from .models import Recipe, Ingredient, IngredientItem


class IngredientItemInline(admin.TabularInline):
    """Встроенная форма для работы с ингредиентами рецепта.

    Attributes:
        model (Model): Связанная модель IngredientItem
        readonly_fields (list): Только для чтения (единицы измерения)
        fields (list): Отображаемые поля во встроенной форме

    Methods:
        ingredient_unit: Получает человекочитаемое название единицы измерения
    """
    model = IngredientItem
    readonly_fields = ['ingredient_unit']
    fields = ['ingredient', 'ingredient_unit', 'quantity']

    def ingredient_unit(self, obj: IngredientItem) -> str:
        """Возвращает отображаемое название единицы измерения ингредиента."""
        return obj.ingredient.get_unit_display()

    ingredient_unit.short_description = 'Единица измерения'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Административная панель для управления рецептами."""
    inlines = [IngredientItemInline]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Административная панель для управления ингредиентами.

    Атрибуты:
        list_display (list): Поля для отображения в списке:
            - name: Название ингредиента
            - unit: Единица измерения
            - price_per_unit: Цена за единицу
            - calories_per_unit: Калорийность за единицу
    """
    list_display = ['name', 'unit', 'price_per_unit', 'calories_per_unit']
