from django.contrib import admin
from django.urls import path, include
from import_export.admin import ExportMixin
from django.shortcuts import redirect
from tests_app.models import Test

urlpatterns = [
    path('admin/', admin.site.urls),  # админка
    path('', lambda request: redirect('auth_view')),  
    path('', include('users_app.urls')),  
    path('tests/', include('tests_app.urls')),  
    path('admin/tests_app/test/import/', ExportMixin, name='tests_app_test_import'),
]

