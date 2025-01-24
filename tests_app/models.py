from django.db import models
from django.contrib.auth.models import User
from django.views.generic import ListView, FormView
from django.shortcuts import redirect
from django.utils import timezone

# Если KeyForm у вас определён в другом месте, нужно скорректировать импорт.
# from .forms import KeyForm  # Пример, как можно импортировать, если форма в forms.py или другом месте

class Subject(models.Model):
    name = models.CharField("Название предмета", max_length=100)

    def __str__(self):
        return self.name


class TestListView(ListView):
    """
    Класс-вьюха для отображения списка тестов, доступных конкретному пользователю.
    Обычно вьюхи располагают в файле views.py, но здесь оставим в models.py, как у вас в примере.
    """
    model = 'Test'  # Можно передавать строкой, если класс Test описан ниже
    template_name = 'tests_app/test_list.html'
    context_object_name = 'tests'

    def get_queryset(self):
        # Импортируем модель Test и TestResult внутри метода, 
        # чтобы избежать ошибок, связанных с порядком объявлений
        from .models import Test, TestResult

        user = self.request.user
        granted_tests = TestResult.objects.filter(
            user=user, 
            access_granted=True
        ).values_list('test', flat=True)

        return Test.objects.filter(id__in=granted_tests)


class EnterKeyView(FormView):
    """
    Вьюха для обработки ввода ключа доступа к тесту.
    Обычно хранится в views.py, но здесь для примера остаётся в models.py.
    """
    template_name = 'tests_app/enter_key.html'
    form_class = None  # <-- тут нужно указать вашу форму, напр. KeyForm

    def form_valid(self, form):
        # Импортируем Test, TestResult внутри метода, чтобы избежать проблем порядка объявлений
        from .models import Test, TestResult

        access_key = form.cleaned_data['access_key']
        user = self.request.user
        try:
            test = Test.objects.get(access_key=access_key)
            # Проверяем, есть ли уже запись для данного теста
            result, created = TestResult.objects.get_or_create(user=user, test=test)
            if not result.access_granted:
                result.access_granted = True
                result.save()
            return redirect('test_list')  # Перенаправление к списку тестов
        except Test.DoesNotExist:
            form.add_error('access_key', 'Неверный ключ доступа')
            return self.form_invalid(form)


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
