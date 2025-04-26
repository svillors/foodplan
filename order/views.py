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
        duration=subscription.duration,
        include_breakfast=subscription.include_breakfast,
        include_lunch=subscription.include_lunch,
        include_dinner=subscription.include_dinner,
        include_dessert=subscription.include_dessert,
        persons=subscription.persons_count,
    )
    # Здесь можно добавить аллергенные поля, если нужно
    return redirect('orders:payment', order_id=order.id)

@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    # Базовая цена за месяц
    base_price = 599
    # Считаем итоговую сумму
    total = base_price * order.persons * order.duration
    return render(request, 'order/create.html', {'order': order, 'total': total})

def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    amount = 599 * order.persons * order.duration
    return render(request, 'order/payment_success.html', {'order': order, 'amount': amount})

def payment_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order/payment_cancel.html', {'order': order})

def apply_promo_code(request):
    if request.method == 'POST' and request.is_ajax():
        # Здесь логика проверки промокода
        # Пример:
        code = request.POST.get('code')
        order_id = request.POST.get('order_id')
        # По умолчанию скидка 0%
        discount = 0
        new_amount = 599  # или вычисли на основе заказа
        if code == 'TEST10':
            discount = 10
            new_amount = int(new_amount * 0.9)
            return JsonResponse({'success': True, 'discount': discount, 'new_amount': new_amount})
        else:
            return JsonResponse({'success': False, 'error': 'Промокод недействителен'})
    return JsonResponse({'success': False, 'error': 'Некорректный запрос'})

@login_required
def payment_demo(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    # Если у заказа есть поле amount:
    amount = getattr(order, 'amount', None)
    # Если нет — вычисли сумму:
    if amount is None:
        base_price = 599
        amount = base_price * order.persons * order.duration
    return render(request, 'order/payment_demo.html', {'order': order, 'amount': amount})

