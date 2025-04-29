from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from order.views import create_order

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('foodapp.urls')),
    path('', include('accounts.urls')),
    path('', include('order.urls')),
    path('recipe/', include('recipes.urls')),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name ='password_reset_complete'),
    path('order/', create_order, name='order'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
