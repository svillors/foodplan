from django.urls import path
from .views import register_view, login_view, lk_view, subscribe, logout_view
from django.contrib.auth.views import LogoutView
from order.views import create_order


urlpatterns = [

    path('register/', register_view, name='register'),
    path('auth/', login_view, name='auth'),
    path('lk/', lk_view, name='lk'),
    path('logout/', logout_view, name='logout'),
    # path('activate-subscription/', activate_subscription, name='activate_subscription'),
    path('subscribe/', subscribe, name='subscribe'),
    # path('', include('django.contrib.auth.urls')),
    path('order/', create_order, name='order'),
    

]
