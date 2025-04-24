from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.utils.timezone import now

from .forms import CustomUserCreationForm
from recipes.models import DailyMenu, Recipe


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

        return render(request, 'registration.html', {'form': form})

    else:
        form = CustomUserCreationForm()
        return render(request, 'registration.html', {'form': form})


def login_view(request):
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
    user = request.user
    dailymenu, created = DailyMenu.objects.get_or_create(
        user=user,
        date=date
    )
    if created:
        # тут должен быть фильтр по аллергиям, но пока не завезли
        recipes = Recipe.objects.order_by('?')[:3]
        dailymenu.recipes.add(*recipes)
    

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
        'subscription_active': user.subscription_active if hasattr(user, 'subscription_active') else False,
        'subscription_end': user.subscription_end if hasattr(user, 'subscription_end') else None,
    }
    return render(request, 'lk.html', context)
    # return render(request, 'lk.html', context={'menu': dailymenu})

@login_required
@require_POST
def activate_subscription(request):
    user = request.user
    user.subscription_active = True
    user.subscription_end = timezone.now() + timezone.timedelta(days=30)
    user.save()
    return redirect('lk')


# def subscribe(request):
#     return render(request, 'subscription.html')

