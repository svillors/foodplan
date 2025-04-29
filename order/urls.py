from .views import create_order, payment, payment_details, change_order
from accounts.views import lk_view
from django.urls import path

urlpatterns = [
    path('order/', create_order, name='create_order'),
    path('lk/', lk_view, name='lk'),
    path('payment/', payment, name='payment'),
    path('payment_details/', payment_details, name='payment_details'),
    path('change_order/', change_order, name='change_order'),
]