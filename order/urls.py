from .views import create_order, payment, payment_details
from accounts.views import lk_view
from django.urls import path

urlpatterns = [
    path('order/', create_order, name='create_order'),
    path('payment/<int:order_id>/', payment, name='payment'),
    path('lk/', lk_view, name='lk'),
    path('payment/details/<int:order_id>/', payment_details, name='payment_details'),
]