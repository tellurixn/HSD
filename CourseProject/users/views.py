from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from main.models import *
from .forms import RegistrationForm

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST or None, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            if form.cleaned_data.get('role') == 'candidate':


                new_resume = JobResume(surname=form.cleaned_data.get('surname'),
                                       name=form.cleaned_data.get('name'),
                                       patronymic=form.cleaned_data.get('patronymic'),
                                       gender=form.cleaned_data.get('gender'),
                                       phone_number=form.cleaned_data.get('phone'),
                                       adress=form.cleaned_data.get('address'),
                                       birthday=form.cleaned_data.get('dob'),
                                       photo=form.cleaned_data.get('photo'),
                                       position=form.cleaned_data.get('position'),
                                       work_experience=form.cleaned_data.get('experience'))
                new_resume.save()
                new_candidate = Candidate(id_job_resume=new_resume)
                new_candidate.save()
                if form.cleaned_data.get('edu_name') != '':
                    edu = EducationalData(educational_institute=form.cleaned_data.get('edu_name'),
                                          receipt_date=form.cleaned_data.get('edr'),
                                          expiration_date=form.cleaned_data.get('ede'))
                    edu.save()
                    candidate_education = Candidateeducation(id_educational_data=edu, id_candidate=new_candidate)
                    candidate_education.save()

                user = AppUser(username=form.cleaned_data.get('username'),
                               password=form.cleaned_data.get('password'),
                               id_candidate=new_candidate,
                               id_role=Role.objects.get(id_role=3),
                               id_worker=None)
                user.set_password(form.cleaned_data.get('password'))
                user.save()
            else:
                pass


            return redirect('/users/login/')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


