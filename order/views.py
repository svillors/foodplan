from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import OrderForm
from .models import Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def create_order(request):
    if request.method == 'POST':
        print(f"[POST data]: {request.POST}")
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            form.save_m2m()
            return redirect('payment', order_id=order.id)
        else:
            print(f"[Form errors]: {form.errors}")
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        form = OrderForm(initial={'duration': 1, 'persons': 1})

    return render(request, 'order.html', {'form': form})


@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        if 'edit_order' in request.POST:
            return redirect('create_order')
        if 'confirm_payment' in request.POST:
            return redirect('payment_details', order_id=order.id)
    
    return render(request, 'payment.html', {
        'order': order,
        'can_edit': not order.is_paid
    })


@login_required
def payment_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    company_info = {
        'name': 'Foodplan',
        'address': 'ул. Ленина, 10',
        'city_country': 'Москва, Россия',
        'phone': '+7 (495) 123-45-67',
    }
    if request.method == 'POST':
        order.is_paid = True
        order.save()

        user = request.user
        user.subscription_active = True
        user.subscription_end = timezone.now() + timezone.timedelta(days=30 * order.duration)
        user.save()

        messages.success(request, 'Оплата прошла успешно! Подписка активирована.')
        return redirect('lk')
    
    return render(request, 'payment_details.html', {
        'order': order,
        'company_info': company_info,
    })