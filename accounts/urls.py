from django.urls import path
from .views import register_view, login_view, lk_view, subscribe, change_recipe
from django.contrib.auth.views import LogoutView
from order.views import create_order


urlpatterns = [
    path('register/', register_view, name='register'),
    path('auth/', login_view, name='auth'),
    path('lk/', lk_view, name='lk'),
    path('lk/change_recipe/<int:pk>', change_recipe, name='change_one_recipe'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('subscribe/', subscribe, name='subscribe'),
    path('order/', create_order, name='order'),
]
