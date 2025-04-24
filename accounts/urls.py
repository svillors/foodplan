from django.urls import path
from .views import register_view, login_view, lk_view, activate_subscription, subscribe
from django.contrib.auth.views import LogoutView


urlpatterns = [

    path('register/', register_view, name='register'),
    path('auth/', login_view, name='auth'),
    path('lk/', lk_view, name='lk'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('activate-subscription/', activate_subscription, name='activate_subscription'),
    path('subscribe/', subscribe, name='subscribe')

]
