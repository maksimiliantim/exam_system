# exam_system/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
urlpatterns = [
    path('admin/', admin.site.urls),  # Админка
    path('', lambda request: redirect('auth_view')),  # Перенаправление на auth/
    path('', include('users_app.urls')),  # Общая страница входа и регистрации
    path('tests/', include('tests_app.urls')),  # Тесты (пользовательская панель)
]

