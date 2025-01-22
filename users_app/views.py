from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm  # Убедитесь, что SignUpForm определён
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('auth_view')  # Перенаправляем на страницу входа
# Представление для регистрации
class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

# Общая страница для входа и регистрации
def auth_view(request):
    if request.method == 'POST':
        # Проверяем, что пользователь нажал "Войти"
        if 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)

                # Проверяем, является ли пользователь администратором
                if user.username == 'nol' and user.check_password('5ELtWll1'):
                    return redirect('/admin/')  # Перенаправляем в админку
                else:
                    return redirect('/tests/dashboard/')  # Перенаправляем на пользовательскую панель
            else:
                return render(request, 'users_app/auth.html', {'error': 'Неверное имя пользователя или пароль.'})

        # Проверяем, что пользователь нажал "Зарегистрироваться"
        elif 'signup' in request.POST:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            # Создаём нового пользователя
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password=password)
                login(request, user)
                return redirect('/tests/dashboard/')  # После регистрации перенаправляем на панель пользователя
            else:
                return render(request, 'users_app/auth.html', {'error': 'Пользователь с таким именем уже существует.'})

    return render(request, 'users_app/auth.html')


