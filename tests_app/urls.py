from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.TestListView.as_view(), name='test_list'),  # список всех тестов
    path('dashboard/', views.user_dashboard, name='user_dashboard'),  # Панель пользователя
    path('enter-key/', views.EnterKeyView.as_view(), name='enter_key'),
    path('test/<int:pk>/', views.TestDetailView.as_view(), name='test_detail'),
    path('test/<int:pk>/start/', views.start_test, name='start_test'),
    path('test/<int:pk>/take/', views.take_test, name='take_test'),
    path('test/<int:pk>/result/', views.test_result, name='test_result'),
    path('test/<int:pk>/review/', views.test_review, name='test_review'),
    path('auth/', auth_view, name='auth'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

