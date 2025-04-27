import random

from recipes.models import Recipe


def get_random_recipe_by_prefers(meal, user_tags, exclude_pk=None):
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


def meal_index(recipe, meal_tags):
    tag_names = [tag.name for tag in recipe.tags.all()]
    for i, meal in enumerate(meal_tags):
        if meal in tag_names:
            return i
    return len(meal_tags)
