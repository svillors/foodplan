from django.urls import path
from foodapp import views

urlpatterns = [
    path('', views.index, name='index'),
]
