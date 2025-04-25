from .views import create_order, payment
from django.urls import path

urlpatterns = [
    path('order/', create_order, name='create_order'),
    path('payment/<int:order_id>/', payment, name='payment'),
]