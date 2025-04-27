from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from recipes.models import Tag

from .forms import OrderForm
from .models import Order
from recipes.models import DailyMenu


@login_required
def create_order(request):
    MENU_TYPES = [
        ('classic', 'Классическое'),
        ('low', 'Низкоуглеводное'),
        ('veg', 'Вегетарианское'),
        ('keto', 'Кето'),
    ]

    # Сопоставление кода меню из формы и имени тега в базе
    MENU_TYPE_NAME_MAP = {
        'classic': 'классическое',
        'low': 'низкоуглеводное',
        'veg': 'вегетарианское',
        'keto': 'кето',
    }

    allerges_tags = Tag.objects.filter(category='allergy')
    allowed_food_intake_names = ['завтрак', 'обед', 'ужин', 'десерт']
    food_intake = Tag.objects.filter(name__in=allowed_food_intake_names, category='food_intake')
    print(f"[food_intake]{food_intake}")
    print(f"[allerges_tags]{allerges_tags}")
    
    if request.method == 'POST':
        data = request.POST.copy()

        # Обработка имен с квадратными скобками (если в шаблоне используются)
        if 'food_intake[]' in data:
            data.setlist('food_intake', data.getlist('food_intake[]'))
            del data['food_intake[]']

        if 'prefers[]' in data:
            data.setlist('prefers', data.getlist('prefers[]'))
            del data['prefers[]']

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
                # другие поля формы, если нужны
            }
            
            # Сохраняем ID тега меню
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
def payment(request):
    order_data = request.session.get('order_data')
    if not order_data:
        return redirect('create_order')

    # Получаем объекты тегов из БД, используя ID из СЕССИИ
    menu_tag = Tag.objects.filter(id=request.session.get('menu_tag_id')).first() #тег меню
    
    # Для prefers, food_intake и allergies
    # prefers_tags = Tag.objects.filter(id__in=order_data.get('prefers', []))
    # food_intake_tags = Tag.objects.filter(id__in=order_data.get('food_intake', []))
    # allergies_tags = Tag.objects.filter(id__in=order_data.get('allergies', []))
    
    # Формируем контекст с объектами
    context = {
        # отображает тег меню, если есть
        'menu_tag': menu_tag,  # Передаем menu_tag напрямую

        # эти переменные больше не нужны, тк мы их НЕ сохраняем в заказе
        #'prefers': prefers_tags,
        #'food_intake_tags': food_intake_tags,
        #'allergies': allergies_tags,
        'order': {  # Имитируем объект Order для шаблона
            'include_breakfast': order_data.get('include_breakfast', False),
            'include_lunch': order_data.get('include_lunch', False),
            'include_dinner': order_data.get('include_dinner', False),
            'include_dessert': order_data.get('include_dessert', False),
        },
        'can_edit': True
    }

    if request.method == 'POST':
        if 'edit_order' in request.POST:
            return redirect('create_order')
        if 'confirm_payment' in request.POST:
            return redirect('payment_details')

    return render(request, 'payment.html', context)


@login_required
def payment_details(request):
    print(f"[ПРОВЕРКА] Текущие теги: {request.user.prefers.all()}")
    order_data = request.session.get('order_data')
    company_info = {
        'name': 'Foodplan',
        'address': 'ул. Ленина, 10',
        'city_country': 'Москва, Россия',
        'inn': '7707083893',
        'ogrn': '1027739828071',
        'rs': '40702810338050007559',
        'bank': 'ПАО СБЕРБАНК',
        'bik': '044525225',
        'krs': '30101810400000000225',
        'phone': '+7 (495) 123-45-67',
    }
    if not order_data:
        return redirect('create_order')

    if request.method == 'POST':
        order_data = request.session.get('order_data', {})

        order = Order.objects.create(
            user=request.user,
            persons=order_data.get('persons', 1),
            is_paid=True,
            menu_type=order_data.get('menu_type'),
            duration=order_data.get('duration', 1),
            include_breakfast=order_data.get('include_breakfast', False),
            include_lunch=order_data.get('include_lunch', False),
            include_dinner=order_data.get('include_dinner', False),
            include_dessert=order_data.get('include_dessert', False)
        )

        tags_to_add = []

        # Меню 
        if 'menu_tag_id' in request.session:  # Убедитесь, что это сохраняется в create_order
            menu_tag = Tag.objects.get(id=request.session['menu_tag_id'])
            tags_to_add.append(menu_tag)

        # Аллергии 
        allergy_ids = order_data.get('allergies', [])
        allergy_tags = Tag.objects.filter(id__in=allergy_ids)
        tags_to_add.extend(allergy_tags)

        # Приёмы пищи
        food_intake_ids = order_data.get('food_intake', [])
        food_intake_tags = Tag.objects.filter(id__in=food_intake_ids)
        tags_to_add.extend(food_intake_tags)

        # 3. Синхронизируем с пользователем
        user = request.user
        user.prefers.set(tags_to_add)  # Добавляем все теги сразу
        user.subscription_active = True
        user.subscription_end = timezone.now() + timezone.timedelta(days=30 * int(order.duration))
        user.save()

        # 4. Очистка
        DailyMenu.objects.filter(user=user, date=timezone.now().date()).delete()
        del request.session['order_data']
        if 'menu_tag_id' in request.session:
            del request.session['menu_tag_id']

        messages.success(request, 'Оплата прошла успешно! Подписка активирована.')
        return redirect('lk')

    return render(request, 'payment_details.html', {
        'order_data': order_data,
        'company_info': company_info,
    })

@login_required
def change_order(request):
    user = request.user
    # Получаем активные предпочтения пользователя
    user_prefers = user.prefers.all()  # Получаем все текущие предпочтения пользователя

    # Ищем последний оплаченный заказ пользователя, если он есть
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
            # Получаем новый тип меню из формы
            menu_type = form.cleaned_data.get('menu_type')

            # Список тегов для обновления
            tags_to_add = []

            # Добавляем тег типа меню, если он выбран
            if menu_type:
                tag_name = MENU_TYPE_TAGS.get(menu_type)
                if tag_name:
                    try:
                        menu_tag = Tag.objects.get(name__iexact=tag_name, category='menu_type')
                        tags_to_add.append(menu_tag)
                    except Tag.DoesNotExist:
                        messages.error(request, f'Тег для типа меню "{tag_name}" не найден.')
                        return redirect('change_order')

            # Получаем ID тегов из POST (предополагаем, что это id для приемов пищи и аллергий)
            meal_allergy_tag_ids = request.POST.getlist('prefers')
            if meal_allergy_tag_ids:
                tags_to_add.extend(Tag.objects.filter(id__in=meal_allergy_tag_ids))

            # Обновляем теги пользователя, используя set()
            user.prefers.set(tags_to_add)

            messages.success(request, 'Настройки подписки обновлены!')
            return redirect('lk')
        else:
            messages.error(request, 'Исправьте ошибки в форме.')
    else:
        # Если запрос GET, заполняем форму данными из последнего заказа
        if last_order:
            form = OrderForm(instance=last_order)
        else:
            form = OrderForm()

    return render(request, 'change_order.html', {
        'form': form,
        'MENU_TYPES': Order.MENU_TYPES,
        'meal_tags': Tag.objects.filter(category='food_intake'),
        'allergy_tags': Tag.objects.filter(category='allergy'),
        'current_tag_ids': user_prefers.values_list('id', flat=True),
    })