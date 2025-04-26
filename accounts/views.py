from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.utils.timezone import now
from .forms import CustomUserCreationForm
from recipes.models import DailyMenu, Recipe
from order.models import Order
from subscriptions.models import Subscription


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


@login_required
def lk_view(request):
    user = request.user

    # Ищем активную подписку
    active_subscription = Subscription.objects.filter(
        user=user,
        is_active=True,
        end_date__gte=timezone.now().date()
    ).order_by('-end_date').first()

    subscription_active = bool(active_subscription)
    subscription_end = active_subscription.end_date if active_subscription else None

    # Формируем меню только если подписка активна
    final_recipes = []
    meal_tags = ['завтрак', 'обед', 'ужин', 'десерт']
    if subscription_active:
        # Здесь твоя логика формирования меню для пользователя
        # Например, на сегодня:
        date = timezone.now().date()
        dailymenu, created = DailyMenu.objects.get_or_create(user=user, date=date)
        if created or not dailymenu.recipes.exists():
            # ... твоя логика подбора рецептов ...
            pass
        final_recipes = dailymenu.recipes.all()
    # Если подписки нет — меню пустое

    if request.method == 'POST':
        new_first_name = request.POST.get('first_name')
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
        'subscription_end': subscription_end,
        'menu': final_recipes,
        'meal_tags': meal_tags
    }
    return render(request, 'lk.html', context)


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


def logout_view(request):
    logout(request)
    return redirect('/?logged_out=1')
