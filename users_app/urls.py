from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Импортируем views для использования auth_view
from django.contrib.auth.views import LogoutView
from .views import auth_view, SignUpView
from .views import LogoutView
urlpatterns = [
    path('auth/', views.auth_view, name='auth_view'),  # Общая страница для входа и регистрации
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),  # Исправлено
]

