from .views import create_order, payment, payment_success, payment_cancel, payment_demo
from django.urls import path

app_name = 'orders'

urlpatterns = [
    path('order/<int:subscription_id>/', create_order, name='create'),
    path('payment/<int:order_id>/', payment, name='payment'),
    path('payment/success/<int:order_id>/', payment_success, name='payment_success'),
    path('payment/cancel/<int:order_id>/', payment_cancel, name='payment_cancel'),
    path('payment/demo/<int:order_id>/', payment_demo, name='payment_demo'),
]