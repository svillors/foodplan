from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import OrderForm
from .models import Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from recipes.models import Tag

@login_required
def create_order(request):
    menu_tags = Tag.objects.filter(name__in=[
        'Классическое', 'Низкоуглеводное', 'Вегетарианское', 'Кето'
    ])
    allerges_tags = Tag.objects.filter(name__in=[
        'без морепродуктов',
        'без мяса', 
        'без зерновых',
        'без продуктов пчеловодства',
        'без орехов и бобовых',
        'без молочных продуктов'])
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order_data = form.cleaned_data.copy()
            for key, value in order_data.items():
                if hasattr(value, 'all'):
                    order_data[key] = list(value.values_list('id', flat=True))
            request.session['order_data'] = order_data
            return redirect('payment')
        else:
            print(f"[Form errors]: {form.errors}")
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        form = OrderForm(initial={'duration': 1, 'persons': 1})

    return render(request, 'order.html', {
        'form': form, 
        'menu_tags': menu_tags, 
        'allerges_tags': allerges_tags
        })

@login_required
def payment(request):
    order_data = request.session.get('order_data')
    if not order_data:
        return redirect('create_order')

    if request.method == 'POST':
        if 'edit_order' in request.POST:
            return redirect('create_order')
        if 'confirm_payment' in request.POST:
            return redirect('payment_details')

    return render(request, 'payment.html', {
        'order_data': order_data,
        'can_edit': True
    })


@login_required
def payment_details(request):
    order_data = request.session.get('order_data')
    company_info = {
        'name': 'Foodplan',
        'address': 'ул. Ленина, 10',
        'city_country': 'Москва, Россия',
        'phone': '+7 (495) 123-45-67',
    }
    if not order_data:
        return redirect('create_order')

    if request.method == 'POST':
        order_data = request.session.get('order_data', {})
        m2m_fields = {}
        data = order_data.copy()
        # Отделяем m2m-поля (например, allergies)
        for key, value in list(data.items()):
            if isinstance(value, list):
                m2m_fields[key] = data.pop(key)
        # Создаём заказ без m2m-полей
        order = Order.objects.create(
            user=request.user,
            is_paid=True,
            **data
        )
        # Устанавливаем значения для m2m-полей
        for key, value in m2m_fields.items():
            getattr(order, key).set(value)
        print(f"[order.prefers.all() после set]: {list(order.prefers.all())}")
        # Синхронизация предпочтений пользователя с заказом
        user1 = request.user
        print(f"[user1]{user1}")
        user1.prefers.set(order.prefers.all())
        print(list(user1.prefers.all()))    # Выходит при оформление заказа []
        user1.save()
        
        user = request.user
        user.subscription_active = True
        user.subscription_end = timezone.now() + timezone.timedelta(days=30 * int(order.duration))
        user.save()
        del request.session['order_data']
        messages.success(request, 'Оплата прошла успешно! Подписка активирована.')
        return redirect('lk')

    return render(request, 'payment_details.html', {
        'order_data': order_data,
        'company_info': company_info,
    })


@login_required
def change_order(request):
    user = request.user
    last_order = user.orders.filter(is_paid=True).last()

    if not last_order:
        messages.error(request, 'У вас нет активной подписки для изменения.')
        return redirect('lk')

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=last_order)
        if form.is_valid():
            order = form.save()
            user.prefers.set(order.prefers.all())
            user.save()
            messages.success(request, 'Подписка успешно изменена!')
            return redirect('lk')
        else:
            messages.error(request, 'Ошибка в форме. Пожалуйста, проверьте введенные данные.')
    else:
        form = OrderForm(instance=last_order)
    return render(request, 'change_order.html', {'form': form})