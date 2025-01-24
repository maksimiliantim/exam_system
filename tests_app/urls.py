from django.urls import path
from . import views

urlpatterns = [
    path('', views.TestListView.as_view(), name='test_list'),  # список всех тестов
    path('dashboard/', views.user_dashboard, name='user_dashboard'),  # Панель пользователя
    path('enter-key/', views.EnterKeyView.as_view(), name='enter_key'),
    path('test/<int:pk>/', views.TestDetailView.as_view(), name='test_detail'),
    path('test/<int:pk>/start/', views.start_test, name='start_test'),
    path('test/<int:pk>/take/', views.take_test, name='take_test'),
    path('test/<int:pk>/result/', views.test_result, name='test_result'),
    path('test/<int:test_id>/review/', views.test_review, name='test_review'),
]

