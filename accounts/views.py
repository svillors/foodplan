import random

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.utils.timezone import now
from .forms import CustomUserCreationForm
from recipes.models import DailyMenu, Recipe
from order.models import Order


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.save()

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('lk')
            else:
                messages.error(request, 'Ошибка аутентификации.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    else:
        form = CustomUserCreationForm()

    return render(request, 'registration.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('lk')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('lk')
            else:
                messages.error(request, 'Аккаунт неактивен.')
        else:
            messages.error(request, 'Неверные email или пароль.')

    return render(request, 'auth.html')


def lk_view(request):
    user = request.user
    date = now().date()
    
    # Получение последнего оплаченного заказа
    try:
        last_order = user.orders.filter(is_paid=True).latest('created_at')
    except Order.DoesNotExist:
        last_order = None
    
    # Формирование meal_tags на основе последнего заказа (если есть)
    if last_order:
        meal_tags = []
        if last_order.include_breakfast: 
            meal_tags.append('завтрак')
        if last_order.include_lunch: 
            meal_tags.append('обед')
        if last_order.include_dinner: 
            meal_tags.append('ужин')
        if last_order.include_dessert: 
            meal_tags.append('десерт')
    # else:
    #     meal_tags = ['завтрак', 'обед', 'ужин', 'десерт']
    meal_tags = ['завтрак', 'обед', 'ужин', 'десерт']
    # Работа с DailyMenu
    dailymenu, created = DailyMenu.objects.get_or_create(
        user=user,
        date=date
    )
    
    final_recipes = []
    
    def meal_index(recipe):
        tag_names = [tag.name for tag in recipe.tags.all()]
        for i, meal in enumerate(meal_tags):
            if meal in tag_names:
                return i
        return len(meal_tags)
    
    # Проверяем активна ли подписка и не истекла ли
    subscription_active = user.subscription_active and user.subscription_end and user.subscription_end >= date
    
    # Генерация меню
    if created:
        if subscription_active:
            user_tags_all = [tag.name for tag in user.prefers.all()]
            user_tags = [tag for tag in user_tags_all if tag not in meal_tags]
            valid_meals = [tag for tag in user_tags_all if tag in meal_tags]

            selected_recipes = []
            for meal in valid_meals or meal_tags:
                recipes = (
                    Recipe.objects
                    .filter(tags__name=meal)
                    .distinct()
                )
                filtered_recipes = []
                for recipe in recipes:
                    recipe_tag_names = list(
                        recipe.tags.values_list('name', flat=True))

                    if all(
                        tag_name in recipe_tag_names for tag_name in user_tags
                    ):
                        filtered_recipes.append(recipe)

                recipe = random.choice(filtered_recipes) if filtered_recipes else None

                if recipe:
                    selected_recipes.append(recipe)

            final_recipes = sorted(selected_recipes, key=meal_index)
            dailymenu.recipes.add(*final_recipes)
        else:
            final_recipes = Recipe.objects.order_by('?')[:1]
            dailymenu.recipes.add(*final_recipes)
    else:
        final_recipes = sorted(dailymenu.recipes.all(), key=meal_index)
    
    # Обновление данных пользователя
    if request.method == 'POST':
        new_first_name = request.POST.get('first_name')
        if new_first_name:
            user.first_name = new_first_name
            try:
                user.save()
                messages.success(request, 'Данные успешно обновлены!')
            except Exception as e:
                messages.error(request, f'Ошибка: {str(e)}')
        return redirect('lk')
    
    # Формирование контекста
    context = {
        'user': user,
        'subscription_active': subscription_active,
        'subscription_end': user.subscription_end,
        'menu': final_recipes,
        'meal_tags': meal_tags,
        'dailymenu': dailymenu,
        'order': last_order,  # Передаем последний оплаченный заказ
    }
    return render(request, 'lk.html', context)


def change_recipe(request, pk):
    user = request.user
    date = now().date()
    meal_tags = ['завтрак', 'обед', 'ужин', 'десерт']
    user_tags_all = [tag.name for tag in user.prefers.all()]
    user_tags = [tag for tag in user_tags_all if tag not in meal_tags]
    dailymenu = DailyMenu.objects.get(user=user, date=date)
    old_order = get_object_or_404(Recipe, pk=pk)
    reqiured_meal = [
        tag.name for tag in old_order.tags.all() if tag.name in meal_tags
    ].pop()
    new_recipes = (
        Recipe.objects
        .filter(tags__name=reqiured_meal)
        .exclude(pk=pk)
        .prefetch_related('tags')
    )
    filtered_recipes = []
    for recipe in new_recipes:
        recipe_tag_names = list(
            recipe.tags.values_list('name', flat=True))
        if all(
            tag_name in recipe_tag_names for tag_name in user_tags
        ):
            filtered_recipes.append(recipe)

        new_recipe = random.choice(filtered_recipes) if filtered_recipes else None
    dailymenu.recipes.remove(old_order)
    dailymenu.recipes.add(new_recipe)
    dailymenu.change_count -= 1
    dailymenu.save()
    messages.success(
        request,
        f'Поменяли рецепт! Осталось смен: {dailymenu.change_count}' if dailymenu.change_count >= 1 else 'Поменяли рецепт! На сегодня смены кончились'
    )
    return redirect('lk')


@login_required
@require_POST
def activate_subscription(request):
    user = request.user
    user.subscription_active = True
    user.subscription_end = timezone.now() + timezone.timedelta(days=30)
    user.save()
    return redirect('lk')


def subscribe(request):
    return render(request, 'subscription.html')
