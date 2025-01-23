from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Subject, Test, Question, Answer, TestResult

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'access_key')

@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    list_display = ('text', 'test')
    search_fields = ('text',)

@admin.register(Answer)
class AnswerAdmin(ImportExportModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    search_fields = ('text',)

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'passed')
