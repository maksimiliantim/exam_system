from django.contrib import admin
from import_export.admin import ExportMixin
from .models import Test, Question, Answer, TestResult

@admin.register(Test)
class TestAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('title', 'subject', 'start_datetime', 'end_datetime')
    search_fields = ('title', 'subject__name')

@admin.register(Question)
class QuestionAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('text', 'test')
    search_fields = ('text',)

@admin.register(Answer)
class AnswerAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    search_fields = ('text',)

@admin.register(TestResult)
class TestResultAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'passed')
    search_fields = ('user__username', 'test__title')


admin.site.register(Test)
admin.site.register(Subject)
admin.site.register(TestResult)
