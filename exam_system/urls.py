from django.contrib import admin
from django.urls import path, include
from import_export.admin import ExportMixin
from django.shortcuts import redirect
from .models import Test
urlpatterns = [
    path('admin/', admin.site.urls),  # админка
    path('', lambda request: redirect('auth_view')),  # перенаправление на auth/
    path('', include('users_app.urls')),  # общая страница входа и регистрации
    path('tests/', include('tests_app.urls')),  # тесты (пользовательская панель)
]

