from .models import Order
from django import forms
from recipes.models import Tag


class OrderForm(forms.ModelForm):
    """Форма для создания/редактирования заказа.

    Attributes:
        prefers (ModelMultipleChoiceField): Выбор предпочтений в тегах
        food_intake (ModelMultipleChoiceField): Приемы пищи для включения
        meal_tags (ModelMultipleChoiceField): Теги приемов пищи
        allergies (ModelMultipleChoiceField): Выбор аллергенов
        menu_type (ChoiceField): Радиокнопки выбора типа меню

    Methods:
        __init__: Кастомизация атрибутов виджетов
    """
    prefers = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    food_intake = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(name__in=['завтрак', 'обед', 'ужин', 'десерт']),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    meal_tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(category='food_intake'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    allergies = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(category='allergy'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    MENU_TYPES = [
        ('classic', 'Классическое'),
        ('low', 'Низкоуглеводное'),
        ('veg', 'Вегетарианское'),
        ('keto', 'Кето'),
    ]

    menu_type = forms.ChoiceField(
        choices=MENU_TYPES,
        widget=forms.RadioSelect(attrs={'class': 'd-none'}),
        label='Тип меню',
        required=True,
    )

    class Meta:
        model = Order
        fields = [
            'allergies', 'menu_type', 'include_breakfast', 'include_lunch',
            'include_dinner', 'include_dessert', 'prefers', 'food_intake',
        ]
        widgets = {
            'menu_type': forms.RadioSelect,
            'include_breakfast': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_lunch': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_dinner': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_dessert': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'allergies': forms.CheckboxSelectMultiple(),
            'food_intake': forms.CheckboxSelectMultiple(),
            'prefers': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        """Инициализация формы с кастомизацией стилей."""
        super().__init__(*args, **kwargs)
        self.fields['menu_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['prefers'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['food_intake'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['allergies'].widget.attrs.update({'class': 'form-check-input'})