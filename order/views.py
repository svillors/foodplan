from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import OrderForm
from .models import Order, Allergy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from recipes.models import Order


# @login_required
# def create_order(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.user = request.user
#             order.save()
#             form.save_m2m()  # Сохраняем аллергии
            
#             # Перенаправляем на страницу оплаты
#             return redirect('payment', order_id=order.id)
#         else:
#             messages.error(request, 'Исправьте ошибки в форме')
#     else:
#         form = OrderForm()
    
#     return render(request, 'order.html', {'form': form})
@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            form.save_m2m()
            return redirect('payment', order_id=order.id) 
        else:
            print("Form errors:", form.errors)  # Проверьте консоль
            messages.error(request, 'Ошибка в данных формы')
    else:
        form = OrderForm()
    
    return render(request, 'order.html', {'form': form})

@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        # Здесь должна быть интеграция с платежной системой
        # Временная имитация успешной оплаты
        order.is_paid = True
        order.save()
        
        # Активируем подписку
        user = request.user
        user.subscription_active = True
        user.subscription_end = timezone.now() + timezone.timedelta(days=30*order.duration)
        user.save()
        
        return redirect('lk')
    
    return render(request, 'subscription.html', {'order': order})

