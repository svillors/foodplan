from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from recipes.models import Recipe


def index(request: HttpRequest) -> HttpResponse:
    """Отображает главную страницу со случайными рецептами в карусели.

    Получает 5 случайных рецептов из базы данных используя случайную сортировку,
    и рендерит главный шаблон с контекстом карусели.

    Args:
        request (HttpRequest): Объект HTTP-запроса от пользователя.

    Returns:
        HttpResponse: Отрендеренный шаблон index.html с контекстом:
            - carousel_recipes: 5 случайных рецептов
    """
    carousel_recipes = Recipe.objects.order_by('?')[:5]
    return render(request, "index.html", {'carousel_recipes': carousel_recipes})
