from django.urls import path

from .views import recipe_details

urlpatterns = [
    path("<int:pk>/", recipe_details, name="recipe_detail"),
]
