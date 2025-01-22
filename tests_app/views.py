# tests_app/views.py
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
        # Если пользователь не вошёл, перенаправляем на страницу логина
        return redirect('login')  # Убедитесь, что маршрут логина указан в users_app.urls
    else:
        # Проверяем, является ли пользователь администратором
        if request.user.username == 'nol' and request.user.email == 'iojuga@mail.ru':
            return redirect('/admin/')  # Перенаправляем в админку
        else:
            # Все остальные пользователи считаются обычными
            return redirect('user_dashboard')  # Панель пользователя

def user_dashboard(request):
    tests = Test.objects.all()  # Можно фильтровать только доступные тесты
    return render(request, 'tests_app/user_dashboard.html', {'tests': tests})
class TestListView(ListView):
    model = Test
    template_name = 'tests_app/test_list.html'
    context_object_name = 'tests'

    def get_queryset(self):
        # Можно выводить только те тесты, у которых ещё не вышло время, и т.д.
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
    # Проверяем, доступен ли тест по дате/времени
    if not test_obj.is_available_now():
        return render(request, 'tests_app/not_available.html', {"test": test_obj})

    # Проверяем, не проходил ли пользователь уже тест (если не хотим давать повтор)
    existing_result = TestResult.objects.filter(user=request.user, test=test_obj).first()
    if existing_result:
        return redirect('test_result', pk=test_obj.pk)

    # Создаём запись о начале теста
    result = TestResult.objects.create(
        user=request.user,
        test=test_obj,
        start_time=timezone.now()
    )
    return redirect('take_test', pk=test_obj.pk)

@login_required
def take_test(request, pk):
    test_obj = get_object_or_404(Test, pk=pk)
    result = TestResult.objects.filter(user=request.user, test=test_obj).first()
    if not result:
        # Если пользователь не «начинал» тест, перенаправляем
        return redirect('start_test', pk=test_obj.pk)

    # Получаем вопросы
    questions = test_obj.questions.all()

    if request.method == 'POST':
        # Обрабатываем присланные ответы
        user_answers = request.POST
        score = 0
        total = questions.count()

        for question in questions:
            correct_ids = question.answers.filter(is_correct=True).values_list('id', flat=True)
            selected_id = user_answers.get(f"question_{question.id}")
            if selected_id:
                selected_id = int(selected_id)
                if selected_id in correct_ids:
                    score += 1

        final_score = int((score / total) * 100)
        result.score = final_score
        result.end_time = timezone.now()
        result.passed = (final_score >= test_obj.passing_score)
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
