from django.contrib import admin

from .models import Recipe, Ingredient, IngredientItem, Tag, DailyMenu


class IngredientItemInline(admin.TabularInline):
    model = IngredientItem
    fields = ['ingredient', 'quantity']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientItemInline]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(DailyMenu)
class DailyMenuAdmin(admin.ModelAdmin):
    pass