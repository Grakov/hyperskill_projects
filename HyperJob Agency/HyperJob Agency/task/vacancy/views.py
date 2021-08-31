from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse

from vacancy.forms import VacancyForm
from vacancy.models import Vacancy


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'agency/index.html')


class VacanciesView(View):
    def get(self, request, *args, **kwargs):
        vacancies_set = Vacancy.objects.all()
        return render(request, "agency/vacancies.html", context={"vacancies": vacancies_set})


class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    success_url = '/'
    template_name = 'agency/login.html'


class CustomSignupView(CreateView):
    form_class = UserCreationForm
    success_url = '/login'
    template_name = 'agency/signup.html'


class CreateVacancy(View):
    def check_auth(self, user):
        return user.is_authenticated and user.is_staff

    def post(self, request, *args, **kwargs):
        if not self.check_auth(request.user):
            return HttpResponse("403 (Forbidden)", status=403)

        vacancy_form = VacancyForm(request.POST)
        if vacancy_form.is_valid():
            description = vacancy_form.cleaned_data['description']
            Vacancy.objects.create(description=description, author=request.user)
            return redirect('/home')
        else:
            vacancy_form.add_error("description", "Description length should be between 1 and 1024 characters")
            return self.get(request, vacancy_form)

    def get(self, request, vacancy_form=VacancyForm(), *args, **kwargs):
        if not self.check_auth(request.user):
            return HttpResponse("403 (Forbidden)", status=403)

        return render(request, "agency/create.html", context={
            "page_title": "Create vacancy",
            "form": vacancy_form
        })
