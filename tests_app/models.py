from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Subject(models.Model):
    name = models.CharField("Название предмета", max_length=100)

    def __str__(self):
        return self.name

class Test(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name="Предмет"
    )
    title = models.CharField("Название теста", max_length=200)
    start_datetime = models.DateTimeField("Дата и время начала")
    end_datetime = models.DateTimeField("Дата и время окончания")
    duration_minutes = models.PositiveIntegerField("Время на прохождение (мин.)", default=60)
    passing_score = models.PositiveIntegerField("Проходной балл (0–100)", default=50)
    access_key = models.CharField("Ключ доступа", max_length=50, unique=True)

    def __str__(self):
        return f"{self.title} ({self.subject})"

    def is_available_now(self):
        now = timezone.now()
        return self.start_datetime <= now <= self.end_datetime

class Question(models.Model):
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Тест"
    )
    text = models.TextField("Текст вопроса")

    def __str__(self):
        return f"Вопрос: {self.text[:50]}..."

class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Вопрос"
    )
    text = models.CharField("Текст ответа", max_length=500)
    is_correct = models.BooleanField("Правильный ответ", default=False)

    def __str__(self):
        return f"Ответ: {self.text[:50]}..."

class TestResult(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        verbose_name="Тест"
    )
    score = models.PositiveIntegerField("Набранные баллы", default=0)
    start_time = models.DateTimeField("Время начала теста", auto_now_add=True)
    end_time = models.DateTimeField("Время завершения теста", null=True, blank=True)
    passed = models.BooleanField("Пройден?", default=False)
    user_answers = models.JSONField("Ответы пользователя", default=dict)
    access_granted = models.BooleanField("Доступ разрешен", default=False)

    def __str__(self):
        return f"{self.user.username} -> {self.test.title} ({self.score} баллов)"
