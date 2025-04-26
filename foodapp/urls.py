from django.urls import path
from foodapp import views
from recipes.views import recipe_details

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/<int:pk>/', recipe_details, name='recipe_detail')
]
