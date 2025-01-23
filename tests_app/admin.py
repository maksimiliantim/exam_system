from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Question, Answer, Test, Subject, TestResult

@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    list_display = ('text', 'test')
    search_fields = ('text',)

@admin.register(Answer)
class AnswerAdmin(ImportExportModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    search_fields = ('text',)

admin.site.register(Test)
admin.site.register(Subject)
admin.site.register(TestResult)
