from .models import Order
from django import forms


class OrderForm(forms.ModelForm):
    PERSONS_CHOICES = [(i, str(i)) for i in range(1, 7)]

    persons = forms.ChoiceField(
        choices=PERSONS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
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
            'menu_type', 'duration', 'include_breakfast', 'include_lunch',
            'include_dinner', 'include_dessert', 'persons', 'allergies'
        ]
        widgets = {
            'menu_type': forms.RadioSelect,
            'duration': forms.Select(attrs={'class': 'form-select'}),
            'include_breakfast': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_lunch': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_dinner': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'include_dessert': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'persons': forms.Select(attrs={'class': 'form-select'}),
            'allergies': forms.CheckboxSelectMultiple(),
        }