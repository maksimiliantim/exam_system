from django.contrib import admin
from django.contrib import admin
from import_export.admin import ExportMixin
from .models import Question

@admin.register(Question)
class QuestionAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('id', 'text', 'test')
