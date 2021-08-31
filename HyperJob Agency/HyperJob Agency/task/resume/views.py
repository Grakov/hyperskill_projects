from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse

from resume.forms import ResumeForm
from resume.models import Resume


class ResumesView(View):
    def get(self, request, *args, **kwargs):
        resumes_set = Resume.objects.all()
        return render(request, "agency/resumes.html", context={"resumes": resumes_set})


class CreateResume(View):
    def check_auth(self, user):
        return user.is_authenticated

    def post(self, request, *args, **kwargs):
        if not self.check_auth(request.user):
            return HttpResponse("403 (Forbidden)", status=403)

        resume_form = ResumeForm(request.POST)
        if resume_form.is_valid():
            description = resume_form.cleaned_data['description']
            Resume.objects.create(description=description, author=request.user)
            return redirect('/home')
        else:
            resume_form.add_error("description", "Description length should be between 1 and 1024 characters")
            return self.get(request, resume_form)

    def get(self, request, resume_form=ResumeForm(), *args, **kwargs):
        if not self.check_auth(request.user):
            return HttpResponse("403 (Forbidden)", status=403)

        return render(request, "agency/create.html", context={
            "page_title": "Create resume",
            "form": resume_form
        })


class HomeView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('/vacancy/new')
            else:
                return redirect('/resume/new')

            #return render(request, 'agency/home.html', context={'user': request.user})
        else:
            return redirect('/login')
