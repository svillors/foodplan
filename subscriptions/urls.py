from django.urls import path
from . import views

app_name = 'subscriptions'
 
urlpatterns = [
    path('entry/', views.subscription_entrypoint, name='entry'),
    path('create/', views.create_subscription, name='create'),
    path('my/', views.my_subscription, name='my'),
] 