from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import OrderForm
from .models import Order, Allergy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse


@login_required
def create_order(request, subscription_id):
    # Получаем подписку
    from subscriptions.models import Subscription
    subscription = Subscription.objects.get(id=subscription_id, user=request.user)
    # Создаём заказ на основе подписки
    order = Order.objects.create(
        user=request.user,
        subscription=subscription,
        menu_type=subscription.menu_type,
        duration=1,  # всегда 1 месяц
        include_breakfast=subscription.include_breakfast,
        include_lunch=subscription.include_lunch,
        include_dinner=subscription.include_dinner,
        include_dessert=subscription.include_dessert,
        persons=1,  # всегда 1 персона
    )
    # Здесь можно добавить аллергенные поля, если нужно
    return redirect('orders:payment', order_id=order.id)

@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    # Базовая цена за месяц
    base_price = 599
    # Считаем итоговую сумму
    total = base_price * 1 * 1
    return render(request, 'order/create.html', {'order': order, 'total': total})

def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    amount = 599 * 1 * 1
    return render(request, 'order/payment_success.html', {'order': order, 'amount': amount})

@login_required
def payment_cancel(request, order_id):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    else:
        order = get_object_or_404(Order, id=order_id)
    base_price = 599
    amount = base_price * 1 * 1
    return render(request, 'order/payment_cancel.html', {'order': order, 'amount': amount})

@login_required
def payment_demo(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    # Если у заказа есть поле amount:
    amount = getattr(order, 'amount', None)
    # Если нет — вычисли сумму:
    if amount is None:
        base_price = 599
        amount = base_price * 1 * 1
    return render(request, 'order/payment_demo.html', {'order': order, 'amount': amount})

