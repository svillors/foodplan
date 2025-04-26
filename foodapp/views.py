from django.shortcuts import render
from recipes.models import Recipe


def index(request):
    carousel_recipes = Recipe.objects.order_by('-id')[:5]
    return render(request, "index.html", {'carousel_recipes': carousel_recipes})
