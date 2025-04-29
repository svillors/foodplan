import random
from typing import Optional, List

from recipes.models import Recipe


def get_random_recipe_by_prefers(
    meal: str,
    user_tags: List[str],
    exclude_pk: Optional[int] = None
) -> Optional[Recipe]:
    """Возвращает случайный рецепт, соответствующий заданным критериям.

    Args:
        meal (str): Категория приема пищи (например, 'завтрак', 'обед')
        user_tags (List[str]): Список предпочитаемых тегов пользователя
        exclude_pk (Optional[int]): ID рецепта для исключения из выбора

    Returns:
        Optional[Recipe]: Случайный рецепт или None, если подходящих нет

    Raises:
        ValueError: Если не найдено ни одного подходящего рецепта
    """
    recipes = (
        Recipe.objects
        .filter(tags__name=meal)
        .prefetch_related('tags')
        .distinct()
    )

    if exclude_pk:
        recipes = recipes.exclude(pk=exclude_pk)

    filtered_recipes = []
    for recipe in recipes:
        recipe_tag_names = list(
            recipe.tags.values_list('name', flat=True))

        if all(
            tag_name in recipe_tag_names for tag_name in user_tags
        ):
            filtered_recipes.append(recipe)

    return random.choice(filtered_recipes) if filtered_recipes else None


def meal_index(recipe: Recipe, meal_tags: List[str]) -> int:
    """Определяет порядковый индекс приема пищи для сортировки рецептов.

    Args:
        recipe (Recipe): Объект рецепта для анализа
        meal_tags (List[str]): Список тегов-приемов пищи в порядке сортировки

    Returns:
        int: Индекс первого найденного тега приема пищи из meal_tags.
             Если не найден - возвращает длину списка meal_tags.
    """
    tag_names = [tag.name for tag in recipe.tags.all()]
    for i, meal in enumerate(meal_tags):
        if meal in tag_names:
            return i
    return len(meal_tags)
