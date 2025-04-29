from django.contrib import admin

from .models import Recipe, Ingredient, IngredientItem


class IngredientItemInline(admin.TabularInline):
    model = IngredientItem
    readonly_fields = ['ingredient_unit']
    fields = ['ingredient', 'ingredient_unit', 'quantity']

    def ingredient_unit(self, obj):
        return obj.ingredient.get_unit_display()

    ingredient_unit.short_description = 'Единица измерения'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientItemInline]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit', 'price_per_unit', 'calories_per_unit']
