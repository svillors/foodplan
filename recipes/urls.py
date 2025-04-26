from django.urls import path

from .views import recipe_details, index, recipe_list, privacy_policy, terms_of_use, menu_by_type

app_name = 'recipes'

urlpatterns = [
    path("", index, name="home"),
    path("<int:pk>/", recipe_details, name="recipe_detail"),
    path('list/', recipe_list, name='recipe_list'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('terms-of-use/', terms_of_use, name='terms_of_use'),
    path('menu/<str:menu_type>/', menu_by_type, name='menu_by_type'),
]
