from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from recipes.models import Tag
from django.http import HttpRequest, HttpResponse

from .forms import OrderForm
from .models import Order
from recipes.models import DailyMenu


@login_required
def create_order(request: HttpRequest) -> HttpResponse:
    """Создание нового заказа через форму.

    Args:
        request (HttpRequest): Объект HTTP-запроса. Требуется авторизация.

    Returns:
        HttpResponse: Страница с формой заказа или редирект на оплату.
    """
    MENU_TYPES = [
        ('classic', 'Классическое'),
        ('low', 'Низкоуглеводное'),
        ('veg', 'Вегетарианское'),
        ('keto', 'Кето'),
    ]

    MENU_TYPE_NAME_MAP = {
        'classic': 'классическое',
        'low': 'низкоуглеводное',
        'veg': 'вегетарианское',
        'keto': 'кето',
    }

    allerges_tags = Tag.objects.filter(category='allergy')
    allowed_food_intake_names = ['завтрак', 'обед', 'ужин', 'десерт']
    food_intake = Tag.objects.filter(name__in=allowed_food_intake_names, category='food_intake')

    if request.method == 'POST':
        data = request.POST.copy()

        if 'food_intake[]' in data:
            data.setlist('food_intake', data.getlist('food_intake[]'))
            del data['food_intake[]']

        if 'prefers[]' in data:
            data.setlist('prefers', data.getlist('prefers[]'))
            del data['prefers[]']

        if 'allergies[]' in data:
            data.setlist('allergies', data.getlist('allergies[]'))
            del data['allergies[]']

        form = OrderForm(data)

        if form.is_valid():
            menu_type_value = form.cleaned_data['menu_type']
            menu_tag_name = MENU_TYPE_NAME_MAP.get(menu_type_value)

            if not menu_tag_name:
                messages.error(request, 'Неверный тип меню')
                return redirect('create_order')

            try:
                menu_tag = Tag.objects.get(name__iexact=menu_tag_name, category='menu_type')
                request.session['menu_tag_id'] = menu_tag.id

            except Tag.DoesNotExist:
                messages.error(request, 'Ошибка конфигурации меню')
                return redirect('create_order')

            order_data = {
                'menu_type': menu_type_value,
                'prefers': list(form.cleaned_data['prefers'].values_list('id', flat=True)),
                'food_intake': list(form.cleaned_data['food_intake'].values_list('id', flat=True)),
                'allergies': list(form.cleaned_data.get('allergies', Tag.objects.none()).values_list('id', flat=True)),
            }

            request.session['menu_tag_id'] = menu_tag.id

            request.session['order_data'] = order_data
            messages.success(request, 'Настройки подписки обновлены!')
            return redirect('payment')
        else:
            print(f"[Error]{form.errors}")
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        form = OrderForm()

    return render(request, 'order.html', {
        'form': form,
        'MENU_TYPES': MENU_TYPES,
        'allerges_tags': allerges_tags,
        'food_intake': food_intake,
    })


@login_required
def payment(request: HttpRequest) -> HttpResponse:
    """Обработка страницы оплаты заказа.

    Args:
        request (HttpRequest): Объект запроса с данными заказа в сессии.

    Returns:
        HttpResponse: Страница оплаты или редирект на создание заказа.
    """
    order_data = request.session.get('order_data')
    if not order_data:
        return redirect('create_order')

    def create_new_order():
        order = Order.objects.create(
            user=request.user,
            persons=order_data.get('persons', 1),
            is_paid=False,
            menu_type=order_data.get('menu_type'),
            duration=order_data.get('duration', 1),
            include_breakfast=order_data.get('include_breakfast', False),
            include_lunch=order_data.get('include_lunch', False),
            include_dinner=order_data.get('include_dinner', False),
            include_dessert=order_data.get('include_dessert', False)
        )
        request.session['order_id'] = order.id
        request.session['order_created'] = True
        return order

    if request.session.get('order_created') and request.session.get('order_id'):
        try:
            order = Order.objects.get(id=request.session['order_id'])
        except Order.DoesNotExist:
            order = create_new_order()
    else:
        order = create_new_order()

    context = {
        'order': order,
        'menu_tag': Tag.objects.get(id=request.session.get('menu_tag_id')),
        'food_intake_tags': Tag.objects.filter(id__in=order_data.get('food_intake', [])),
        'allergies_tags': Tag.objects.filter(id__in=order_data.get('allergies', [])),
        'can_edit': True
    }

    if request.method == 'POST':
        if 'edit_order' in request.POST:
            return redirect('create_order')
        if 'confirm_payment' in request.POST:
            return redirect('payment_details')

    return render(request, 'payment.html', context)


@login_required
def payment_details(request: HttpRequest) -> HttpResponse:
    """Завершение процесса оплаты.

    Args:
        request (HttpRequest): Объект запроса с order_id в сессии.

    Returns:
        HttpResponse:
            - Редирект в ЛК с подтверждением оплаты
            - Редирект на создание заказа при отсутствии данных
    """
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('create_order')

    order = Order.objects.get(id=order_id)

    if request.method == 'POST':
        order.is_paid = True
        order.save()

        tags_to_add = []
        if 'menu_tag_id' in request.session:
            tags_to_add.append(Tag.objects.get(id=request.session['menu_tag_id']))

        tags_to_add.extend(Tag.objects.filter(
            id__in=request.session['order_data'].get('allergies', [])
        ))
        tags_to_add.extend(Tag.objects.filter(
            id__in=request.session['order_data'].get('food_intake', [])
        ))

        request.user.prefers.set(tags_to_add)
        request.user.subscription_active = True
        request.user.subscription_end = timezone.now() + timezone.timedelta(
            days=30 * int(order.duration)
        )
        request.user.save()

        del request.session['order_data']
        del request.session['order_id']
        if 'menu_tag_id' in request.session:
            del request.session['menu_tag_id']

        try:
            user = request.user
            date = timezone.now().date()
            DailyMenu.objects.get(user=user, date=date).delete()
        except DailyMenu.DoesNotExist:
            pass

        messages.success(request, f'Оплата прошла успешно! Номер вашего заказа: #{order.id}')
        return redirect('lk')

    context = {
        'order': order,
        'menu_tag': Tag.objects.get(id=request.session.get('menu_tag_id')),
        'food_intake_tags': Tag.objects.filter(id__in=request.session['order_data'].get('food_intake', [])),
        'allergies_tags': Tag.objects.filter(id__in=request.session['order_data'].get('allergies', []))
    }

    return render(request, 'payment_details.html', context)


@login_required
def change_order(request: HttpRequest) -> HttpResponse:
    """Редактирование активной подписки.

    Args:
        request (HttpRequest): Объект запроса авторизованного пользователя.

    Returns:
        HttpResponse: Страница редактирования или редирект в ЛК.
    """
    user = request.user
    user_prefers = user.prefers.all()
    date = timezone.now().date()
    last_order = user.orders.filter(is_paid=True).last()

    MENU_TYPE_TAGS = {
        'classic': 'классическое',
        'low': 'низкоуглеводное',
        'veg': 'вегетарианское',
        'keto': 'кето',
    }

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=last_order)
        if form.is_valid():
            menu_type = form.cleaned_data.get('menu_type')
            tags_to_add = []
            if menu_type:
                tag_name = MENU_TYPE_TAGS.get(menu_type)
                if tag_name:
                    try:
                        menu_tag = Tag.objects.get(name__iexact=tag_name, category='menu_type')
                        tags_to_add.append(menu_tag)
                    except Tag.DoesNotExist:
                        messages.error(request, f'Тег для типа меню "{tag_name}" не найден.')
                        return redirect('change_order')

            meal_allergy_tag_ids = request.POST.getlist('prefers')
            if meal_allergy_tag_ids:
                tags_to_add.extend(Tag.objects.filter(
                    id__in=meal_allergy_tag_ids)
                )

            user.prefers.set(tags_to_add)

            messages.success(request, 'Настройки подписки обновлены!')
            return redirect('lk')
        else:
            messages.error(request, 'Исправьте ошибки в форме.')
    else:
        if last_order:
            form = OrderForm(instance=last_order)
        else:
            form = OrderForm()
    try:
        DailyMenu.objects.get(user=user, date=date).delete()
    except DailyMenu.DoesNotExist:
        pass

    return render(request, 'change_order.html', {
        'form': form,
        'MENU_TYPES': Order.MENU_TYPES,
        'meal_tags': Tag.objects.filter(category='food_intake'),
        'allergy_tags': Tag.objects.filter(category='allergy'),
        'current_tag_ids': user_prefers.values_list('id', flat=True),
    })
