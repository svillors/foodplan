from django.shortcuts import render, redirect
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
    try:
        last_order = user.orders.latest('created_at')
        meal_tags = []
        if last_order.include_breakfast: meal_tags.append('завтрак')
        if last_order.include_lunch: meal_tags.append('обед')
        if last_order.include_dinner: meal_tags.append('ужин')
        if last_order.include_dessert: meal_tags.append('десерт')
    except Order.DoesNotExist:  # Теперь Order будет распознан
        meal_tags = ['завтрак', 'обед', 'ужин', 'десерт']
        
    user = request.user
    date = now().date()
    user = request.user
    dailymenu, created = DailyMenu.objects.get_or_create(
        user=user,
        date=date
    )
    final_recipes = []
    meal_tags = ['завтрак', 'обед', 'ужин', 'десерт']

    def meal_index(recipe):
        tag_names = [tag.name for tag in recipe.tags.all()]
        for i, meal in enumerate(meal_tags):
            if meal in tag_names:
                return i
        return 999

    if created:
        if user.subscription_active:
            user_tags = user.prefers.all()

            meals = [
                tag for tag in user.prefers.all() if tag.name in meal_tags
            ]
            selected_recipes = []
            for meal in meals:
                recipe = (
                    Recipe.objects
                    .filter(tags__name=meal, tags__in=user_tags)
                    .order_by('?')
                    .prefetch_related('tags')
                    .first()
                )
                if recipe:
                    selected_recipes.append(recipe)
            final_recipes = sorted(selected_recipes, key=meal_index)
            dailymenu.recipes.add(*final_recipes)
        else:
            final_recipes = Recipe.objects.order_by('?')[:1]
            dailymenu.recipes.add(*final_recipes)
    else:
        final_recipes = sorted(dailymenu.recipes.all(), key=meal_index)

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
        'menu': final_recipes
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
