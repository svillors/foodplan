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
from .utils import get_random_recipe_by_prefers, meal_index


MEAL_TAGS = ['завтрак', 'обед', 'ужин', 'десерт']


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
    try:
        last_order = user.orders.filter(is_paid=True).latest('created_at')
        can_change_order = True
    except Order.DoesNotExist:
        last_order = None
        can_change_order = False

    dailymenu, created = DailyMenu.objects.get_or_create(
        user=user,
        date=date
    )

    subscription_active = (
        user.subscription_active
        and user.subscription_end
        and user.subscription_end >= date
    )

    final_recipes = []
    if created:
        if subscription_active:
            user_tags_all = [tag.name for tag in user.prefers.all()]
            user_tags = [tag for tag in user_tags_all if tag not in MEAL_TAGS]
            valid_meals = (
                [tag for tag in user_tags_all if tag in MEAL_TAGS]
                or MEAL_TAGS
            )
            selected_recipes = []
            for meal in valid_meals:
                recipe = get_random_recipe_by_prefers(meal, user_tags)
                if recipe:
                    selected_recipes.append(recipe)
            final_recipes = sorted(
                selected_recipes,
                key=lambda recipe: meal_index(recipe, MEAL_TAGS)
            )
            dailymenu.recipes.add(*final_recipes)
        else:
            final_recipes = Recipe.objects.order_by('?')[:1]
            dailymenu.recipes.add(*final_recipes)
    else:
        final_recipes = sorted(
            dailymenu.recipes.all(),
            key=lambda recipe: meal_index(recipe, MEAL_TAGS)
        )
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

    context = {
        'user': user,
        'subscription_active': subscription_active,
        'subscription_end': user.subscription_end,
        'menu': final_recipes,
        'meal_tags': MEAL_TAGS,
        'dailymenu': dailymenu,
        'order': last_order,
        'can_change_order': can_change_order,
        # 'user_menu_tags': user_menu_tags,
        # 'user_allergy_tags': user_allergy_tags,
        # 'user_food_intake': user_food_intake,
    }
    return render(request, 'lk.html', context)


def change_recipe(request, pk):
    user = request.user
    date = now().date()
    user_tags_all = [tag.name for tag in user.prefers.all()]
    user_tags = [tag for tag in user_tags_all if tag not in MEAL_TAGS]
    dailymenu = DailyMenu.objects.get(user=user, date=date)
    old_order = get_object_or_404(Recipe, pk=pk)
    reqiured_meal = [
        tag.name for tag in old_order.tags.all() if tag.name in MEAL_TAGS
    ].pop()
    new_recipe = get_random_recipe_by_prefers(reqiured_meal, user_tags, pk)
    dailymenu.recipes.remove(old_order)
    dailymenu.recipes.add(new_recipe)
    dailymenu.change_count -= 1
    dailymenu.save()
    messages.success(
        request,
        (
            f'Поменяли рецепт! Осталось смен: {dailymenu.change_count}'
            if dailymenu.change_count >= 1
            else 'Поменяли рецепт! На сегодня смены кончились'
        )
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
