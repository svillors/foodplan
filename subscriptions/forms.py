from django import forms
from .models import Subscription


class SubscriptionForm(forms.ModelForm):
    """Форма для создания и редактирования подписки."""
    
    class Meta:
        model = Subscription
        fields = [
            'menu_type', 'duration',
            'include_breakfast', 'include_lunch', 'include_dinner', 'include_dessert',
            'persons_count',
            'exclude_fish', 'exclude_meat', 'exclude_grains',
            'exclude_honey', 'exclude_nuts', 'exclude_dairy',
        ]
        widgets = {
            'menu_type': forms.RadioSelect(),
            'duration': forms.Select(attrs={'class': 'form-select'}),
            'persons_count': forms.Select(attrs={'class': 'form-select'},
                                         choices=[(i, i) for i in range(1, 7)]),
        } 