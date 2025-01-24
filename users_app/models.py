from tests_app.models import Test, Question, Answer, TestResult
from django.db import models
class Question(models.Model):
    test = models.ForeignKey('tests_app.Test', on_delete=models.CASCADE)
    text = models.TextField()
