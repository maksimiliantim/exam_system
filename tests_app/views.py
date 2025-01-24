from django.views.generic import ListView, FormView

class TestListView(ListView):
    model = Test
    template_name = 'tests_app/test_list.html'
    context_object_name = 'tests'

    def get_queryset(self):
        user = self.request.user
        granted_tests = TestResult.objects.filter(user=user, access_granted=True).values_list('test', flat=True)
        return Test.objects.filter(id__in=granted_tests)

class EnterKeyView(FormView):
    template_name = 'tests_app/enter_key.html'
    form_class = KeyForm

    def form_valid(self, form):
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
