from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.utils import timezone
from .models import Test, TestResult, Question, Answer
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def home_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    else:
        if request.user.username == 'nol' and request.user.email == 'iojuga@mail.ru':
            return redirect('/admin/')  
        else:
            return redirect('user_dashboard')  

def user_dashboard(request):
    results = TestResult.objects.filter(user=request.user, access_granted=True)
    granted_tests = [result.test.id for result in results]  # Список ID доступных тестов
    tests = Test.objects.all()  # Все тесты
    return render(request, 'tests_app/user_dashboard.html', {
        'tests': tests,  # Полный список тестов
        'granted_tests': granted_tests  # Тесты с доступом
    })
class TestListView(ListView):
    model = Test
    template_name = 'tests_app/test_list.html'
    context_object_name = 'tests'

    def get_queryset(self):
        return Test.objects.all()

class KeyForm(forms.Form):
    access_key = forms.CharField(label="Ключ доступа", max_length=50)

class EnterKeyView(FormView):
    template_name = 'tests_app/enter_key.html'
    form_class = KeyForm

    def form_valid(self, form):
        access_key = form.cleaned_data['access_key']
        try:
            test = Test.objects.get(access_key=access_key)
            # Создаем или обновляем запись TestResult
            result, created = TestResult.objects.get_or_create(user=self.request.user, test=test)
            result.access_granted = True
            result.save()
            return redirect('test_detail', pk=test.pk)
        except Test.DoesNotExist:
            form.add_error('access_key', 'Неверный ключ доступа')
            return self.form_invalid(form)
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
        return f"{self.user.username} -> {self.test.title} : {self.score} баллов"
    def form_valid(self, form):
        access_key = form.cleaned_data['access_key']
        try:
            test = Test.objects.get(access_key=access_key)
            return redirect('test_detail', pk=test.pk)
        except Test.DoesNotExist:
            form.add_error('access_key', 'Неверный ключ доступа')
            return self.form_invalid(form)

class TestDetailView(DetailView):
    model = Test
    template_name = 'tests_app/test_detail.html'
    context_object_name = 'test'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test_obj = self.object
        context['is_available'] = test_obj.is_available_now()
        return context

@login_required
def start_test(request, pk):
    test_obj = get_object_or_404(Test, pk=pk)

    # Проверяем, доступен ли тест
    if not test_obj.is_available_now():
        return render(request, 'tests_app/not_available.html', {"test": test_obj})

    # Проверяем, есть ли у пользователя доступ к тесту
    result = TestResult.objects.filter(user=request.user, test=test_obj).first()
    if result and not result.access_granted:
        return redirect('enter_key')  # Перенаправляем на ввод ключа

    # Если результат уже существует, перенаправляем к результату
    if result:
        return redirect('test_result', pk=test_obj.pk)

    # Создаем запись о начале теста
    result = TestResult.objects.create(
        user=request.user,
        test=test_obj,
        start_time=timezone.now(),
        access_granted=True  # Предполагаем, что ключ уже введен
    )
    return redirect('take_test', pk=test_obj.pk)

@login_required
def take_test(request, pk):
    test_obj = get_object_or_404(Test, pk=pk)
    result = TestResult.objects.filter(user=request.user, test=test_obj).first()
    if not result:
        return redirect('start_test', pk=test_obj.pk)

    questions = test_obj.questions.all()

    if request.method == 'POST':
        user_answers = {}
        score = 0
        total = questions.count()

        for question in questions:
            correct_ids = question.answers.filter(is_correct=True).values_list('id', flat=True)
            selected_id = request.POST.get(f"question_{question.id}")
            user_answers[str(question.id)] = selected_id
            if selected_id and int(selected_id) in correct_ids:
                score += 1

        final_score = int((score / total) * 100)
        result.score = final_score
        result.end_time = timezone.now()
        result.passed = (final_score >= test_obj.passing_score)
        result.user_answers = user_answers  
        result.save()

        return redirect('test_result', pk=test_obj.pk)

    return render(request, 'tests_app/test_take.html', {
        'test': test_obj,
        'questions': questions,
    })
@login_required
def test_result(request, pk):
    test_obj = get_object_or_404(Test, pk=pk)
    result = TestResult.objects.filter(user=request.user, test=test_obj).first()
    if not result:
        return redirect('start_test', pk=test_obj.pk)

    return render(request, 'tests_app/test_result.html', {
        'test': test_obj,
        'result': result,
    })
@login_required
def test_review(request, pk):
    test = get_object_or_404(Test, id=pk)
    result = get_object_or_404(TestResult, test=test, user=request.user)

    # Подготовка данных для шаблона
    questions = test.questions.all()
    user_answers = result.user_answers or {}

    questions_with_answers = []
    for question in questions:
        user_answer_id = user_answers.get(str(question.id))
        user_answer = Answer.objects.filter(id=user_answer_id).first()
        correct_answers = question.answers.filter(is_correct=True)
        questions_with_answers.append({
            "question": question,
            "user_answer": user_answer,
            "correct_answers": correct_answers,
        })

    context = {
        "test": test,
        "result": result,
        "questions_with_answers": questions_with_answers,
    }
    return render(request, "tests_app/test_review.html", context)
