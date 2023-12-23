from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import WorkerForm, OrderForm
from .models import *
from datetime import date, timedelta
from django.utils import timezone
import matplotlib.pyplot as plt
import pandas as pd

def index(request):
    sick_leaves = SickLeave.objects.all().filter(expiration_date__gte=date.today())
    vacations = Vacation.objects.all().filter(expiration_date__gte=date.today())
    workers = Worker.objects.all()
    candidates = Candidate.objects.all()

    # вычисляем дату, равную 3 месяца назад
    three_months_ago = timezone.now() - timedelta(days=3 * 30)

    new_workers = EmploymentContract.objects.all().filter(receipt_date__gte=three_months_ago)
    dismissals = Dismissal.objects.all().filter(dismissal_date__gte=three_months_ago)
    new_candidates = Candidate.objects.all()




    data = {
        'sick_counter': len(sick_leaves),
        'vac_counter': len(vacations),
        'worker_counter': len(workers),
        'candidate_counter': len(candidates),
        'new_workers': len(new_workers),
        'dismissals': len(dismissals),
        'new_candidates': len(new_candidates),
    }
    return render(request, 'main/index.html', data)


@login_required
def candidates(request):
    list_candidates = []
    candidates = Candidate.objects.all()

    for candidate in candidates:
        resume = JobResume.objects.get(id_job_resume=candidate.id_job_resume)
        job = resume.position
        fio = resume.surname + ' ' + resume.name + ' ' + resume.patronymic



        list_candidates.append({'fio': fio,
                                'job': job,
                                'id': candidate.id_candidate
                                })

    data = {
        'candidates': list_candidates,
    }


    return render(request, 'main/candidates.html', data)

@login_required
def workers(request):
    list_workers = []
    
    workers = Worker.objects.all()

    for worker in workers:
        try:
            contract = EmploymentContract.objects.get(id_worker=worker.id_worker)
        except EmploymentContract.DoesNotExist:
            continue
        status = ''

        place = PlaceOfWork.objects.get(id_place_of_work=contract.id_place_of_work)

        job_title = JobTitle.objects.get(id_job_title=place.id_job_title)

        fio = worker.surname + ' ' + worker.name + ' ' + worker.patronymic
        vac = Vacation.objects.all().filter(expiration_date__gte=date.today(), id_worker=worker.id_worker)
        sick = SickLeave.objects.all().filter(expiration_date__gte=date.today(), id_worker=worker.id_worker)
        if len(vac) != 0:
            status = 'В отпуске'
        elif len(sick) != 0:
            status = 'На больничном'
        else:
            status = 'Активен'

        list_workers.append({'fio': fio,
                            'job': job_title.name,
                             'status': status,
                             'id': worker.id_worker,
                             })

    data = {
        'workers': list_workers,
    }


    return render(request, 'main/workers.html', data)

@login_required
def orders(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            if form.cleaned_data.get('orderType') == 1: #Отпуск
                pass
            elif form.cleaned_data.get('orderType') == 2: #Прием
                pass
            elif form.cleaned_data.get('orderType') == 3: #Увольнение
                pass


    elif request.method == 'GET':
        form = OrderForm()
        data = {
            'form': form,
        }
        return render(request, 'main/orders.html', data)

@login_required
def concrete_worker(request, id):
    worker = Worker.objects.get(id_worker=id)
    contract = EmploymentContract.objects.get(id_worker=worker.id_worker)
    job = JobTitle.objects.get(id_job_title=contract.id_job_title).name
    subdivision = StructuralSubdivision.objects.get(id_subdivision=contract.id_subdivision).name

    data = {
        'worker': worker,
        'job': job,
        'subdivision': subdivision,
    }

    return render(request, 'main/concrete_worker.html', data)

@login_required
def concrete_candidate(request, id):
    candidate = Candidate.objects.get(id_candidate=id)
    resume = candidate.id_job_resume

    data = {
        'candidate': candidate,
        'resume': resume,
    }

    return render(request, 'main/concrete_candidate.html', data)

@login_required
def edit_worker(request,id):
    error = ''
    if request.method == 'POST':
        instance = get_object_or_404(Worker, id_worker=id)
        form_post = WorkerForm(request.POST or None, request.FILES, instance=instance)

        if form_post.is_valid():
            form_post.save()
            return redirect('/')
        else:
            error = 'Форма заполнена неверными данными!'
            data = {'form': form_post,
                    'error': error
                    }
            print(form_post.errors)
            return render(request, 'main/edit_worker.html', data)
    elif request.method == 'GET':
        worker = Worker.objects.get(id_worker=id)
        form = WorkerForm(instance=worker)


        data = {
            'form': form,
            'error': error
        }
        return render(request, 'main/edit_worker.html', data)


@login_required
def profile(request, id):
    user = request.user

    user_data = Worker.objects.get(id_worker=user.id_worker)
    try:
        contract = EmploymentContract.objects.get(id_worker=user.id_worker)
    except EmploymentContract.DoesNotExist:
        contact = None

    if contact is not None:
        job = JobTitle.objects.get(id_job_title=contract.id_job_title)
        subdivision = StructuralSubdivision.objects.get(id_subdivision=contract.id_subdivision)

        data = {
            'user_data': user_data,
            'job': job.name,
            'subdivision': subdivision.name,
        }
    else:
        data = {
            'user_data': user_data,
        }


    return render(request,'main/worker_page.html', data)


@login_required
def candidate_page(request, id):
    user = request.user

    candidate = Candidate.objects.get(id_candidate=user.id_candidate)
    user_data = JobResume.objects.get(id_job_resume=candidate.id_job_resume)
    edu = Candidateeducation.objects.all().filter(id_candidate=user.id_candidate)

    edu_data = []

    for e in edu:
        edu_data.append(EducationalData.objects.get(id_educational_data=e.id_educational_data))


    data = {
        'user_data': user_data,
        'educations': edu_data,
    }

    return render(request,'main/candidate_page.html', data)