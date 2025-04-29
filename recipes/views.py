from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Recipe


def recipe_details(request: HttpRequest, pk: int) -> HttpResponse:
    """Отображает детальную страницу рецепта с его ингредиентами."""
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.items = recipe.ingredientitem_set.select_related("ingredient")
    return render(request, 'recipe.html', context={'recipe': recipe})
