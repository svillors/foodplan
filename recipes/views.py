from django.shortcuts import render, get_object_or_404
from subscriptions.models import Subscription
from django.utils import timezone

from .models import Recipe


def recipe_details(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.items = recipe.ingredientitem_set.select_related("ingredient")
    return render(request, 'recipe.html', context={'recipe': recipe})

def index(request):
    # твой код
    return render(request, 'recipes/home.html')

def recipe_list(request):
    # твой код
    return render(request, 'recipes/recipe_list.html')

def privacy_policy(request):
    return render(request, 'recipes/privacy_policy.html')

def terms_of_use(request):
    return render(request, 'recipes/terms_of_use.html')

def menu_by_type(request, menu_type):
    recipes = Recipe.objects.filter(tags__name=menu_type)
    subscription_active = False
    if request.user.is_authenticated:
        subscription_active = Subscription.objects.filter(
            user=request.user,
            is_active=True,
            end_date__gte=timezone.now().date()
        ).exists()
    return render(
        request,
        'recipes/menu_by_type.html',
        {
            'recipes': recipes,
            'menu_type': menu_type,
            'subscription_active': subscription_active,
        }
    )
