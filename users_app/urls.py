from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Импортируем views для использования auth_view
from django.contrib.auth.views import LogoutView
from .views import auth_view, SignUpView
from .views import LogoutView
from users_app.views import auth_view
urlpatterns = [
    path('auth/', views.auth_view, name='auth_view'),  
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('auth/', auth_view, name='auth'),
    path('admin/tests_app/test/import/', ExportMixin, name='tests_app_test_import'),
]

