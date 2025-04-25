from .models import Order, Allergy
from django import forms


# class OrderForm(forms.ModelForm):
#     allergies = forms.ModelMultipleChoiceField(
#         queryset=Allergy.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False
#     )

#     class Meta:
#         model = Order
#         fields = [
#             'menu_type', 
#             'duration',
#             'include_breakfast',
#             'include_lunch',
#             'include_dinner',
#             'include_dessert',
#             'persons',
#             'allergies'
#         ]
#         widgets = {
#             'menu_type': forms.RadioSelect(),
#             'duration': forms.Select(attrs={'class': 'form-select'}),
#             'persons': forms.Select(attrs={'class': 'form-select'}),
#         }
        
class OrderForm(forms.ModelForm):
    DURATION_CHOICES = [
        (1, '1 мес.'),
        (3, '3 мес.'),
        (6, '6 мес.'),
        (12, '12 мес.')
    ]
    
    duration = forms.ChoiceField(
        choices=DURATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['user', 'is_paid', 'created_at']
        widgets = {
            'menu_type': forms.RadioSelect(attrs={'class': 'd-none'}),
            'persons': forms.Select(attrs={'class': 'form-select'}),
        }