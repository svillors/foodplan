from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Subscription
from .forms import SubscriptionForm


@login_required
def create_subscription(request):
    """Создание новой подписки."""
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()
            
            # Перенаправляем на оформление заказа
            return redirect('orders:create', subscription_id=subscription.id)
    else:
        form = SubscriptionForm()
    
    context = {
        'form': form,
    }
    return render(request, 'subscriptions/create.html', context)


@login_required
def my_subscription(request):
    """Отображение всех активных подписок пользователя."""
    active_subscriptions = Subscription.objects.filter(
        user=request.user,
        is_active=True
    ).order_by('-created_at')
    
    context = {
        'active_subscriptions': active_subscriptions,
        # Оставляем 'subscription' для обратной совместимости с шаблонами
        'subscription': active_subscriptions.first() if active_subscriptions.exists() else None,
    }
    return render(request, 'subscriptions/my_subscription.html', context)


@login_required
def subscription_entrypoint(request):
    """Редиректит на создание или просмотр подписки в зависимости от наличия."""
    if Subscription.objects.filter(user=request.user, is_active=True).exists():
        return redirect('subscriptions:my')
    return redirect('subscriptions:create')


def create_order(request, subscription_id=None):
    pass 

def menu_by_type(request, menu_type):
    return render(request, 'recipes/menu_by_type.html') 