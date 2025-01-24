# users_app/models.py
from django.db import models
class Question(models.Model):
    test = models.ForeignKey('tests_app.Test', on_delete=models.CASCADE)
    text = models.TextField()
