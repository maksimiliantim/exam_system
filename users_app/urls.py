# users_app/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Импортируем views для использования auth_view

urlpatterns = [
    path('auth/', views.auth_view, name='auth_view'),  # Общая страница для входа и регистрации
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='auth_view'), name='logout'),  # Перенаправление на auth/
    path('signup/', views.SignUpView.as_view(), name='signup'),  # Исправлено
]

