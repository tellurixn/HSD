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
                new_worker = Worker(surname=form.cleaned_data.get('surname'),
                                    name=form.cleaned_data.get('name'),
                                    patronymic=form.cleaned_data.get('patronymic'),
                                    gender=form.cleaned_data.get('gender'),
                                    phone_number=form.cleaned_data.get('phone'),
                                    adress=form.cleaned_data.get('address'),
                                    birthday=form.cleaned_data.get('dob'),
                                    photo=form.cleaned_data.get('photo'),
                                    work_experience=form.cleaned_data.get('experience'))
                new_worker.save()

                if form.cleaned_data.get('pow_name') != '':
                    title = form.cleaned_data.get('job_title')
                    try:
                        new_job = JobTitle.objects.get(name=title)
                    except JobTitle.DoesNotExist:
                        new_job = JobTitle(name=title)
                        new_job.save()


                    subdiv = form.cleaned_data.get('subdivision')
                    try:
                        new_division = StructuralSubdivision.objects.get(name=subdiv)
                    except StructuralSubdivision.DoesNotExist:
                        new_division = StructuralSubdivision(name=subdiv)
                        new_division.save()


                    pow = form.cleaned_data.get('pow_name')
                    ljr = form.cleaned_data.get('ljr')
                    try:
                        new_pow = PlaceOfWork.objects.get(name=pow, id_subdivision=new_division, id_job_title=new_job, reseipt_date=ljr)
                    except PlaceOfWork.DoesNotExist:
                        new_pow = PlaceOfWork(name=pow,id_subdivision=new_division, id_job_title=new_job, reseipt_date=ljr)
                        new_pow.save()


                    if form.cleaned_data.get('role') == 'employee':
                        current_role = Role.objects.get(id_role=2)
                    else:
                        current_role = Role.objects.get(id_role=4)

                    user = AppUser(username=form.cleaned_data.get('username'),
                                   password=form.cleaned_data.get('password'),
                                   id_role=current_role,
                                   id_worker=new_worker)
                    user.set_password(form.cleaned_data.get('password'))
                    user.save()

            return redirect('/users/login/')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


