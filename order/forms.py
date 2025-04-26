from .models import Order
from django import forms
from recipes.models import Tag


class OrderForm(forms.ModelForm):

    PERSONS_CHOICES = [(i, str(i)) for i in range(1, 7)]

    prefers = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    DURATION_CHOICES = [
        (1, '1 мес.'),
    ]
    
    duration = forms.ChoiceField(
        choices=DURATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Order
        fields = [
            'allergies', 'menu_type','include_breakfast', 'include_lunch',
            'include_dinner', 'include_dessert', 'prefers'
        ]
        widgets = {
            'menu_type': forms.RadioSelect,
            'duration': forms.Select(attrs={'class': 'form-select'}),
            'include_breakfast': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_lunch': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_dinner': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_dessert': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # 'persons': forms.Select(attrs={'class': 'form-select'}),
            'allergies': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавьте классы Bootstrap для стилизации формы
        self.fields['menu_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['duration'].widget.attrs.update({'class': 'form-control'})
        self.fields['prefers'].widget.attrs.update({'class': 'form-control'})